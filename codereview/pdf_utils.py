import json
from weasyprint import HTML, CSS
from django.utils.html import escape

def generate_pdf(scan_report):
    try:
        print(f"Raw JSON data: {scan_report.review}")
        reviews = json.loads(f'[{scan_report.review}]')
        print(reviews)

        html_content = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        padding: 30px;
                        max-width: 95%;  /* Set a maximum width for the container */
                        margin: auto;    /* Horizontally center the container */
                    }}
                    h1 {{
                        color: #333366;
                    }}
                    table {{
                        width: 100%;
                        table-layout: fixed;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        border: 1px solid #999;
                        padding: 10px;
                        text-align: left;
                        font-size: 8px;
                        overflow: hidden;    /* Hide overflow content */
                        text-overflow: ellipsis;  /* Display ellipsis for overflow content */
                    }}
                    th {{
                        background-color: 3e77b6;
                        border-top: 1px solid #999;  /* Add top border */
                        border-bottom: 1px solid #999;  /* Add bottom border */
                        font-size: 65%;
                        border: 1px solid #999; /* Complete border for table headers */
                    }}
                    tr:nth-child(even) {{
                        background-color: #f2f2f2;
                    }}
                    .repo-details {{
                        margin-bottom: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Code Review Report</h1>
                    <div class="repo-details">
                        <p><strong>Repository Name:</strong> {escape(scan_report.repository_name)}</p>
                        <p><strong>Scanned At:</strong> {scan_report.scanned_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    <table>
                        <tr>
                            <th>File Name</th>
                            <th>Vulnerability Name</th>
                            <th>Description</th>
                            <th>Severity</th>
                            <th>Vulnerable Code Snippet</th>
                            <th>Remediation</th>
                        </tr>"""

        for review_list in reviews:
            for review in review_list:
                html_content += f"""
                <tr>
                    <td>{escape(review.get('File Name', 'N/A'))}</td>
                    <td>{escape(review.get('Vulnerability Name', 'N/A'))}</td>
                    <td>{escape(review.get('Description', 'N/A'))}</td>
                    <td>{escape(review.get('Severity', 'N/A'))}</td>
                    <td><pre>{escape(review.get('Vulnerable Code Snippet', 'N/A'))}</pre></td>
                    <td>{escape(review.get('Remediation', 'N/A'))}</td>
                </tr>"""

            html_content += """
                        </table>
                    </div>
                </body>
            </html>"""

            html = HTML(string=html_content)
            pdf_file = html.write_pdf(stylesheets=[CSS(string='pre { white-space: pre-wrap; word-wrap: break-word; }')])

            return pdf_file
        
    except Exception as e:
        print(f"An error occurred while generating PDF: {e}")
    return None