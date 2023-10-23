# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO
# from html import escape
# import bleach


# def generate_pdf(scan_report):
#     print("Received scan_report:", scan_report)
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     content = []

#     title_style = styles['Title']

#     content.append(Paragraph('Code Review Report', title_style))

#     # Adding repository details
#     content.append(Spacer(1, 12))
#     content.append(Paragraph(f"Repository Name: {scan_report.repository_name}", styles['Normal']))
#     content.append(Paragraph(f"Scanned At: {scan_report.scanned_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))

#     # Sanitize the GPT response to remove problematic HTML tags
#     sanitized_review = bleach.clean(scan_report.review, tags=[], attributes={})

#     # Add the sanitized GPT response
#     content.append(Paragraph(sanitized_review, styles['Normal']))

#     # Build the PDF with the content list
#     doc.build(content)

#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# def generate_pdf(scan_report):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     content = []

#     title_style = styles['Title']
#     heading_style = styles['Heading1']
#     normal_style = styles['Normal']

#     # Add title
#     content.append(Paragraph('Code Review Report', title_style))

#     # Add repository details
#     content.append(Paragraph(f"Repository Name: {scan_report.repository_name}", normal_style))
#     content.append(Paragraph(f"Scanned At: {scan_report.scanned_at.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))

#     # Split the review into sections by lines
#     sections = scan_report.review.split('\n\n')

#     for section in sections:
#         lines = section.strip().split('\n')

#         if lines:
#             # The first line is considered the heading, and the rest are the content
#             heading = lines[0]
#             content_text = '\n'.join(lines[1:])

#             # Add a spacer for spacing between sections
#             content.append(Spacer(1, 12))

#             # Add the heading in bold
#             content.append(Paragraph(heading, heading_style))

#             content_text_escaped = escape(content_text)

#             # Use KeepTogether to keep the content together as a single paragraph
#             content.append(KeepTogether(Paragraph(content_text_escaped, normal_style)))

#     # Build the PDF with the content list
#     doc.build(content)

#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# import html
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO

# # Function to escape HTML special characters
# def escape(text):
#     return html.escape(text)

# def generate_pdf(scan_report):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)

#     # Styles
#     styles = getSampleStyleSheet()
#     title_style = styles['Title']
#     normal_style = styles['Normal']

#     content = []
#     content.append(Paragraph('Code Review Report', title_style))

#     # Repository details
#     data = [
#         ['Repository Name', scan_report.repository_name, 'Scanned at', scan_report.scanned_at.strftime('%Y-%m-%d %H:%M:%S')]
#     ]
#     t = Table(data, hAlign='LEFT')
#     t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT')]))
#     content.append(t)
#     content.append(Spacer(1, 12))

#     # Parsing the review content
#     review_sections = scan_report.review.split('\n\n')  # split by empty lines

#     for section in review_sections:
#         lines = section.split('\n')
#         if lines[0].startswith("Total number") or lines[0].startswith("File Name"):
#             content.append(Paragraph(lines[0], normal_style))
#             content.append(Spacer(1, 12))
#         else:
#             # Vulnerability name is the first line of the section
#             content.append(Paragraph(f'<b>{lines[0]}</b>', normal_style))
#             content.append(Spacer(1, 6))

#             # Extract the remaining details for the vulnerability
#             vuln_data = lines[1:]
#             data = []
#             for detail in vuln_data:
#                 parts = detail.split(': ', 1)
#                 if len(parts) == 2:
#                     field_name, field_value = parts
#                     safe_value = escape(field_value)
#                     data.append([Paragraph(f'<b>{field_name}</b>', normal_style), Paragraph(safe_value, normal_style)])

#             if data:
#                 t = Table(data, hAlign='LEFT', colWidths=[150, 400])
#                 t.setStyle(TableStyle([
#                     ('BOX', (0, 0), (-1, -1), 1, colors.black),
#                     ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
#                     ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
#                 ]))
#                 content.append(t)
#                 content.append(Spacer(1, 12))

#     doc.build(content)
#     pdf_value = buffer.getvalue()
#     buffer.close()

#     return pdf_value

# import markdown2
# from weasyprint import HTML
# from django.utils.html import escape
# from datetime import datetime

# def generate_pdf(scan_report):
#     try:
#         # Convert Markdown to HTML
#         html_content = markdown2.markdown(scan_report.review, extras=["tables"])

#         # Create an HTML string with styling for the report
#         html_string = f"""
#         <html>
#         <head>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                 }}
#                 h1 {{
#                     color: #333366;
#                 }}
#                 table {{
#                     width: 100%;
#                     border-collapse: collapse;
#                     margin-top: 20px;
#                 }}
#                 th, td {{
#                     border: 1px solid #999;
#                     padding: 8px;
#                     text-align: left;
#                     font-size: 14px;
#                 }}
#                 th {{
#                     background-color: #f2f2f2;
#                 }}
#                 tr:nth-child(even) {{
#                     background-color: #f2f2f2;
#                 }}
#                 .repo-details {{
#                     margin-bottom: 10px;
#                 }}
#             </style>
#         </head>
#         <body>
#             <h1>Code Review Report</h1>
#             <div class="repo-details">
#                 <p><strong>Repository Name:</strong> {escape(scan_report.repository_name)}</p>
#                 <p><strong>Scanned At:</strong> {scan_report.scanned_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
#             </div>
#             {html_content}
#         </body>
#         </html>
#         """

#         # Generate PDF from the HTML content
#         html = HTML(string=html_string)
#         pdf_file = html.write_pdf()

#         return pdf_file
#     except Exception as e:
#         print(f"An error occurred while generating PDF: {e}")
#         return None
    
import json
from weasyprint import HTML, CSS
from django.utils.html import escape

def generate_pdf(scan_report):
    try:
        # Parse the JSON data from the 'review' field.
        print("printing doc")
        reviews = json.loads(f'[{scan_report.review}]')
        print(reviews)  # Adjust this based on the exact format of your JSON data.

        # Begin building the HTML content for the PDF.
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
                    }}
                    h1 {{
                        color: #333366;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        border: 1px solid #999;
                        padding: 10px;
                        text-align: left;
                        font-size: 14px;
                    }}
                    th {{
                        background-color: #f2f2f2;
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

        # Loop through the reviews and add each as a table row.
        for review in reviews:
            html_content += f"""
            <tr>
                <td>{escape(review.get('File Name', 'N/A'))}</td>
                <td>{escape(review.get('Vulnerability Name', 'N/A'))}</td>
                <td>{escape(review.get('Description', 'N/A'))}</td>
                <td>{escape(review.get('Severity', 'N/A'))}</td>
                <td><pre>{escape(review.get('Vulnerable Code Snippet', 'N/A'))}</pre></td>
                <td>{escape(review.get('Remediation', 'N/A'))}</td>
            </tr>"""

        # Close off the HTML tags.
        html_content += """
                    </table>
                </div>
            </body>
        </html>"""

        # Generate PDF from the HTML content.
        html = HTML(string=html_content)
        pdf_file = html.write_pdf(stylesheets=[CSS(string='pre { white-space: pre-wrap; word-wrap: break-word; }')])  # Ensuring code snippets wrap.

        return pdf_file

    except Exception as e:
        print(f"An error occurred while generating PDF: {e}")
        return None