# AZURE_REPO_SEARCH

## Overview

`AZURE_REPO_SEARCH` is a Python script designed to list all projects and their repositories from an Azure DevOps organization, search for email patterns within the repository files, and write the results to CSV files. The script also counts the total number of projects and repositories.

## Prerequisites

- Python 3.6+
- pip (Python package installer)
- Azure DevOps Personal Access Token (PAT)
- Azure DevOps organization name

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/AZURE_REPO_SEARCH.git
    cd AZURE_REPO_SEARCH
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Azure DevOps PAT and organization name:
    ```dotenv
    PAT=your_personal_access_token
    ORG=your_organization_name
    ```

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. The script will create a `results` directory and generate CSV files for each repository containing the email patterns found.

## Configuration

- The script searches for email patterns in files with the following extensions:
    ```python
    valid_file_types = [
        '.sql', '.py', '.java', '.cs', '.json', '.cshtml', '.config', '.js', 
        '.php', '.rb', '.c', '.cpp', '.h', '.txt', '.bat', '.sh', '.xml', 
        '.yaml', '.yml', '.html', '.htm', '.md', '.ts', '.tsx', '.jsx', 
        '.ini', '.log', '.pl', '.swift', '.go', '.r', '.dart', '.scss', 
        '.less', '.asp', '.aspx'
    ]
    ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [requests](https://docs.python-requests.org/en/latest/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [csv](https://docs.python.org/3/library/csv.html)