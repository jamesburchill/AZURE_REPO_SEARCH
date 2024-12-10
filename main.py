#  Copyright (c) 2024 - JamesBurchill.com - See LICENSE for details, otherwise All Rights Reserved
#  File Location: /Users/jamesburchill/Documents/DEV/AZURE_REPO_SEARCH/main.py
#  Last Updated: 2024-12-10, 8:39 a.m.

import base64
import csv
import os
import re

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Personal Access Token (PAT) and organization name from environment variables
pat = os.getenv('PAT')
organization = os.getenv('ORG')

# Define the headers for the API requests
headers = {'Authorization': 'Basic ' + base64.b64encode((':' + pat).encode()).decode()}

def get_data_from_api(url):
    """
    Fetch data from the Azure DevOps API.

    Args:
        url (str): The URL of the API endpoint.

    Returns:
        list: A list of items returned by the API. If the 'value' key is not in the JSON response, return an empty list.
    """
    response = requests.get(url, headers=headers)
    return response.json().get('value', [])

def search_repo(org, proj, repo_id, repo_name, valid_file_types):
    """
    Search a repository for email patterns.

    Args:
        org (str): The organization name.
        proj (str): The project name.
        repo_id (str): The repository ID.
        repo_name (str): The repository name.
        valid_file_types (list): A list of valid file types to search in.

    Returns:
        list: A list of results, where each result is a dictionary containing the repository name, the email found,
              the file where the email was found, and the context of the email.
    """
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    items = get_data_from_api(f'https://dev.azure.com/{org}/{proj}/_apis/git/repositories/{repo_id}/items?recursionLevel=full&api-version=6.0')
    results = []
    for item in items:
        print('.', end='', flush=True)
        if item['gitObjectType'] == 'blob' and os.path.splitext(item['path'])[1].lower() in valid_file_types:
            item_text = requests.get(f'https://dev.azure.com/{org}/{proj}/_apis/git/repositories/{repo_id}/items?path={item["path"]}&api-version=6.0', headers=headers).text
            matches = email_pattern.findall(item_text)
            for match in matches:
                context = item_text[max(0, item_text.find(match) - 30):min(len(item_text), item_text.find(match) + 30)]
                results.append({'repo_name': repo_name, 'email': match, 'file': item['path'], 'context': context})
    return results

def main():
    """
    Search all repositories in a project for email patterns and write the results to CSV files.
    """
    projects = get_data_from_api(f'https://dev.azure.com/{organization}/_apis/projects?api-version=6.0')

    valid_file_types = [
        '.sql',  # SQL scripts
        '.py',  # Python scripts
        '.java',  # Java files
        '.cs',  # C# files
        '.json',  # JSON files
        '.cshtml',  # ASP.NET Razor pages
        '.config',  # Configuration files
        '.js',  # JavaScript files
        '.php',  # PHP scripts
        '.rb',  # Ruby scripts
        '.c',  # C source code
        '.cpp',  # C++ source code
        '.h',  # C/C++ header files
        '.txt',  # Plain text files
        '.bat',  # Batch scripts
        '.sh',  # Shell scripts
        '.xml',  # XML files
        '.yaml',  # YAML files
        '.yml',  # YAML files (alternative extension)
        '.html',  # HTML files
        '.htm',  # HTML files (alternative extension)
        '.md',  # Markdown files
        '.ts',  # TypeScript files
        '.tsx',  # TypeScript React files
        '.jsx',  # JavaScript React files
        '.ini',  # Initialization files
        '.log',  # Log files
        '.pl',  # Perl scripts
        '.swift',  # Swift files
        '.go',  # Go files
        '.r',  # R scripts
        '.dart',  # Dart files
        '.scss',  # SASS files
        '.less',  # LESS files
        '.asp',  # Classic ASP files
        '.aspx',  # ASP.NET files
    ]

    if not os.path.exists('results'):
        os.makedirs('results')

    for proj in projects:
        repos = get_data_from_api(f'https://dev.azure.com/{organization}/{proj["name"]}/_apis/git/repositories?api-version=6.0')
        for repo in repos:
            print(f'\nChecking repository: {repo["name"]}')
            results = search_repo(organization, proj['name'], repo['id'], repo['name'], valid_file_types)
            if results:
                with open(f'results/{repo["name"]}.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['repo_name', 'email', 'file', 'context'])
                    writer.writeheader()
                    writer.writerows(results)
                print(f'\nResults written for repository: {repo["name"]}')

if __name__ == '__main__':
    main()