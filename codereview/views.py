import logging, requests, openai, base64, os
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from github import Github, GithubException
from .models import ScanReport
from django.http import HttpResponse
from .pdf_utils import generate_pdf
from django.http import Http404
import re, json

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

def fetch_repos(request):
    headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
    org_url = f'https://api.github.com/orgs/{settings.GITHUB_ORG_NAME}/repos'

    try:
        response = requests.get(org_url, headers=headers)
        response.raise_for_status()
        repos = response.json()
        context = {'repositories': repos}
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}") 
        context = {'error': str(http_err)}
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        context = {'error': str(err)}

    return render(request, 'codereview/repos.html', context)

def fetch_files_recursive(repo, path):
    contents = repo.get_contents(path)
    file_list = []

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file_list.append(file_content)

    return file_list

def fix_json_commas(json_str):
    try:

        pattern = re.compile(r'}(?!\s*,)(?!\s*])(?=\s*{)')

        fixed_json_str = re.sub(pattern, '},', json_str)

        return fixed_json_str

    except Exception as e:
        print(f"An error occurred: {e}")
        return json_str

@csrf_exempt
def scan_repository(request):
    if request.method == 'POST':
        repo_full_name = request.POST.get('repo_full_name')

        extensions_to_neglect = ['.md']

        g = Github(settings.GITHUB_TOKEN)

        try:
            repo = g.get_repo(repo_full_name)
            all_files = fetch_files_recursive(repo, "")

            reviews = []

            for file in all_files:

                file_extension = os.path.splitext(file.name)[1].lower()

                if file_extension in extensions_to_neglect:
                    continue

                content = base64.b64decode(file.content).decode('utf-8') if file.encoding == 'base64' else file.content

                json_example = '''
                {
                    "File Name": "test.php",
                    "Vulnerability Name": "Command Injection",
                    "Description": "The code uses user-supplied input in a call to the EditUser() function without proper validation, allowing for potential command injection attacks.",
                    "Severity": "High",
                    "Vulnerable Code Snippet": "EditUser(\'email\', $email);",
                    "Remediation": "Use prepared statements or input validation to prevent user-supplied input from being executed as a command."
                },
                '''

                new_prompt = f"""Act as a SAST tool. You have to analyze the below code from {file.path} and provide results for all the unique security vulnerabilities present in the code, in JSON format. The JSON format for these findings should contain: File Name, Vulnerability Name, Description, Severity, Vulnerable Code Snippet, and Remediation.
                
                Make sure to perform the below mentioned 3 modifications when creating the JSON response:

                1. Change all double quotes (") in the Vulnerable code snippets to single quotes (').
                2. Don't leave empty lines between pieces of JSON information.
                3. Do not enclose the JSON bodies within square brackets ([]).

                Example of the expected JSON format: 

                {json_example}

                Here's the code to analyze:

                {content}
                """

                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=new_prompt,
                    max_tokens=2000,
                    temperature=0.5
                )

                print(response)

                reviews.append({
                    'file': file.path,
                    'review': response.choices[0].text.strip()
                })

            consolidated_report1 = "\n".join([review['review'] for review in reviews])

            consolidated_report = "[" + fix_json_commas(consolidated_report1) + "]"

            report = ScanReport(
                repository_name=repo_full_name,
                review=consolidated_report,
            )
            report.save()

            return JsonResponse({'reviews': reviews})

        except GithubException as ge:
            logger.error(f"A GitHub-related error occurred: {str(ge)}")
            return JsonResponse({'error': f'GitHub error: {str(ge)}'}, status=500)

        except openai.error.OpenAIError as oe:
            logger.error(f"An error occurred while communicating with the OpenAI API: {str(oe)}")
            return JsonResponse({'error': f'OpenAI error: {str(oe)}'}, status=500)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Only POST requests are accepted.'}, status=400)    

def show_reports(request):
    reports = ScanReport.objects.all().order_by('-scanned_at')
    return render(request, 'codereview/reports.html', {'reports': reports})

def download_scan_report(request, report_id):
    try:
        scan_report = ScanReport.objects.filter(id=report_id).first()
        if not scan_report:
            raise Http404("ScanReport does not exist")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{scan_report.repository_name}_report.pdf"'

        pdf = generate_pdf(scan_report)
        response.write(pdf)

        return response

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)