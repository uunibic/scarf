[![version](https://img.shields.io/badge/version-1.0-red)](https://www.github.com/uunibic/scarf/)
[![python](https://img.shields.io/badge/python-3.11.6-blue.svg?logo=python&labelColor=yellow)](https://www.python.org/downloads/)
[![django](https://img.shields.io/badge/django-4.2.1-blue.svg?logo=django&labelColor=grey)](https://www.python.org/downloads/)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/uunibic/scarf/)

![SCARF](https://github.com/uunibic/scarf/blob/main/f1baa13d-82ea-4ce4-84c3-0e36b1523333.png)

# SCARF (Source Code Analysis and Review Framework)
SCARF is an open-source SAST tool that harnesses the power of ChatGPT to automatically spot security vulnerabilities and conveniently export them in a report format.

## Overview

SCARF is a utility that enables developers and security professionals to analyze source code for security vulnerabilities. This tool leverages the OpenAI GPT-3.5 Turbo model to provide detailed security analysis reports for your codebase.

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

## Screenshots



## Limitations

## Contributing

I'm excited to have you on board to enhance this project! Since this is my initial foray into working with Django, I'm conscious there might be numerous oversights or areas needing refinement, so your expertise and corrections are pivotal. They not only shape this work but also fuel my learning curve, propelling me toward more ambitious projects. Rest assured, every contribution you make is deeply valued, and it undoubtedly helps make this community an extraordinary space for growth and inspiration.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
