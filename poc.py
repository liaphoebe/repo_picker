#!/usr/bin/python3

import requests
import os
import json
import yaml
from openai import OpenAI
import sys

def fetch_github_repositories(package_name):
    url = f"https://api.github.com/search/repositories"
    params = {'q': package_name, 'sort': 'stars', 'order': 'desc'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        response.raise_for_status()

messages = [{"role": "system", "content": "You're making decisions that drive a program's execution."}]
def query_openai(message, api_key, model="gpt-4o"):
    client = OpenAI(api_key=api_key)
    messages.append({"role": "user", "content": message})
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    content = completion.choices[-1].message.content
    print(content)
    return content

def main():
    if len(sys.argv) < 2:
        print("Please provide the package name.")
        sys.exit(1)

    package_name = sys.argv[1]

    api_key = <openai_api_key>
    if not api_key:
        print("Please set the API_KEY environment variable")
        sys.exit(1)

    repos = fetch_github_repositories(package_name)

    repo_names = [repo['full_name'] for repo in repos]
    formatted_repos = "\n".join(repo_names)

    question = f'''
Which of the following repositories is most likely the upstream source for the {package_name} package? 
Repositories:{formatted_repos}
Answer in this format: {{ candidates: [...] }}
'''

    while True:
        gpt_response = query_openai(question, api_key)
    
        try: 
            output = yaml.safe_load(gpt_response)
            return output
        except yaml.scanner.ScannerError:
            question = "Please respond with only the structured data and nothing else. Do not include ```yaml or the like."


if __name__ == "__main__":
    for _ in range(5):
        main()
