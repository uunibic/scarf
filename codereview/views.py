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

# Set up logging
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
        logger.error(f"HTTP error occurred: {http_err}")  # Changed from print to logging
        context = {'error': str(http_err)}
    except Exception as err:
        logger.error(f"An error occurred: {err}")  # Changed from print to logging
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

@csrf_exempt
def scan_repository(request):
    if request.method == 'POST':
        repo_full_name = request.POST.get('repo_full_name')

        extensions_to_neglect = ['.md']

        # Using GitHub token from settings
        g = Github(settings.GITHUB_TOKEN)

        try:
            repo = g.get_repo(repo_full_name)
            all_files = fetch_files_recursive(repo, "")

            reviews = []  # A list to store reviews of each file.

            # Loop through each file in the repository
            for file in all_files:

                file_extension = os.path.splitext(file.name)[1].lower()

                # Skip files with specific extensions
                if file_extension in extensions_to_neglect:
                    continue

                # Decode the file content from base64 and convert it to a string (if it's encoded).
                content = base64.b64decode(file.content).decode('utf-8') if file.encoding == 'base64' else file.content

                new_prompt = f"""Act as a SAST tool. You have to analyse the below code from {file.path} and provide results for all security vulnerabilities present in the code, in json format that can be used to generate a pdf report. Remember, the clarity, accuracy, and consistency of your report are paramount, as the content will be directly utilised in official documentation.

                The mandatory json format for these findings should contain:
                1. File Name: The exact name of the file from which the code was extracted.
                2. Vulnerability Name: The official designation of the detected security vulnerability.
                3. Description: A detailed explanation of the vulnerability, emphasizing its potential impact and the risks it poses to the software.
                4. Severity: A ranking of the vulnerability's urgency, categorized based on potential harm and exploit likelihood.
                5. Vulnerable Code Snippet: The specific portion of code within the file that is afflicted by the vulnerability.
                6. Remediation: Comprehensive strategies and actions recommended for effectively neutralizing the identified security threat.

                Here's the code:

                {content}"""

                # Call OpenAI API to review the code.
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    # prompt=f"Act as a SAST tool. You have to analyze the below code from {file.path} and provide results for all security vulnerabilities present in the code, in tabular markdown format that can be directly embedded into a pdf report. The format should be File Name, Vulnerability Name, Description, Severity, Vulnerable code snippet and the mitigation steps.\n\n{content}\n",  # Change the prompt as needed
                    prompt=new_prompt,
                    max_tokens=800,
                    temperature=0.5
                )

                print(response)

                # Store the review.
                reviews.append({
                    'file': file.path,
                    'review': response.choices[0].text.strip()  # Extract the actual review text
                })

            # Generate a consolidated report for the entire repository
            consolidated_report = "\n".join([review['review'] for review in reviews])

            # Save the consolidated report in the database
            report = ScanReport(
                repository_name=repo_full_name,
                review=consolidated_report,
            )
            report.save()

            # Respond with the reviews. In production, you might want to store these results in a database instead.
            return JsonResponse({'reviews': reviews})

        except GithubException as ge:
            logger.error(f"A GitHub-related error occurred: {str(ge)}")
            return JsonResponse({'error': f'GitHub error: {str(ge)}'}, status=500)

        except openai.error.OpenAIError as oe:  # Catch OpenAI specific errors
            logger.error(f"An error occurred while communicating with the OpenAI API: {str(oe)}")
            return JsonResponse({'error': f'OpenAI error: {str(oe)}'}, status=500)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Only POST requests are accepted.'}, status=400)    

def show_reports(request):
    reports = ScanReport.objects.all().order_by('-scanned_at')  # Get all reports, newest first
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