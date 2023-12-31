[![version](https://img.shields.io/badge/version-1.0-red)](https://www.github.com/uunibic/scarf/)
[![python](https://img.shields.io/badge/python-3.11.6-blue.svg?logo=python&labelColor=yellow)](https://www.python.org/downloads/)
[![django](https://img.shields.io/badge/django-4.2.1-blue.svg?logo=django&labelColor=grey)](https://www.python.org/downloads/)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/uunibic/scarf/)

![scarf_logo](https://github.com/uunibic/scarf/assets/64989501/db4d9f1c-b77c-41df-be22-cf262256f1df)


# SCARF (Source Code Analysis and Review Framework)
SCARF is an open-source SAST tool that harnesses the power of ChatGPT to automatically spot security vulnerabilities and conveniently export them in a report format.

## Overview

SCARF is a utility that enables developers and security professionals to analyze source code for security vulnerabilities. This tool leverages the OpenAI GPT-3.5 Turbo model to provide detailed security analysis reports for your codebase.

Note: This is a learning project and does not represent my job responsibilities.

## Features

- **GitHub Integration**: Fetch code directly from your GitHub repositories for analysis.
- **Security Analysis**: Automatically identify and report security vulnerabilities in your code.
- **Structured Reports**: Generate downloadable PDF reports with vulnerability details, code snippets, and recommendations.
- **Flexible Configuration**: Customize analysis parameters and prompts for tailored results.

## Prerequisites

Before using the Tool, make sure you have the following prerequisites installed:

- Python 3.x
- Django (for the backend server)
- OpenAI API Key

## Getting Started

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/uunibic/scarf.git

2. Install the required packages.

   ```bash
   pip3 install -r requirements.txt

3. Create a .env file and set the environment variables.

   ```bash
   GITHUB_TOKEN=<Your-Github-Token>
   GITHUB_ORG_NAME=<Github-Org-Name>
   OPENAI_API_KEY=<Your-OpenAI-API-Key>

4. Apply migrations.

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate

5. Run the server.

   ```bash
   python3 manage.py runserver

## Installation Using Docker

If you don't have Docker installed on your system, you can follow up with the [official Docker installation guide.](https://docs.docker.com/get-docker/)

1) Start by cloning the repository:
```
$ git clone https://github.com/uunibic/scarf.git
```
2) Build the Docker image:
```
$ docker build -t scarf --no-cache .
```
3) Build and run Docker container:
```
$ docker run --name scarf -d -p 8000:8000 scarf
```
and now your app is ready to launch at http://127.0.0.1:8000

## Screenshots

#### Repository Dashboard

<img width="1440" alt="sample1" src="https://github.com/uunibic/scarf/assets/64989501/14fe003e-6dd2-4cdf-a8b7-0e20bdee7384">

#### Reports Section

<img width="1440" alt="sample2" src="https://github.com/uunibic/scarf/assets/64989501/3af21fe0-9503-41b4-9148-d6025c9ea259">

#### Sample PDF

[Click Here to View Sample PDF Report](https://github.com/uunibic/scarf/blob/main/sample/Sample_PDF_Report.pdf)

## Limitations

1. **API Rate Limits**: SCARF relies on the ChatGPT API, which is subject to rate limits and usage restrictions imposed by OpenAI. This means there may be limitations on the number of requests or tokens processed within a given timeframe.

2. **Dependence on External Service**: SCARF's core functionality depends on the availability and reliability of the OpenAI API. Any downtime or changes to the API by OpenAI can impact the tool's performance.

3. **Cost Considerations**: While SCARF is open-source, the use of the OpenAI API for extensive analysis can incur costs, especially for large-scale or frequent scanning of codebases.

4. **False Positives/Negatives**: Like all automated analysis tools, SCARF may produce false positives (identifying vulnerabilities that are not real) or false negatives (missing actual vulnerabilities). Human review and validation of results are still essential.

5. **Limited to Code Analysis**: SCARF primarily focuses on source code analysis for security vulnerabilities. It may not cover all aspects of security testing, such as runtime or environmental factors.

6. **Privacy Considerations**: When using SCARF with code repositories, be mindful of potential privacy and security implications, especially when dealing with sensitive code or data.

## Features to be added

* Integration with Jenkins
* PDF Report Enhancement
* Implementing Authentication

## Contributing

I'm excited to have you on board to enhance this project! Since this is my initial foray into working with Django, I'm conscious there might be numerous oversights or areas needing refinement, so your expertise and corrections are pivotal. They not only shape this work but also fuel my learning curve, propelling me toward more ambitious projects. Rest assured, every contribution you make is deeply valued, and it undoubtedly helps make this community an extraordinary space for growth and inspiration.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
