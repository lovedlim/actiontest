import os
import openai
import requests

# GitHub 환경 변수 설정
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
ISSUE_NUMBER = os.getenv('ISSUE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

# 이슈의 내용을 가져오기 위해 GitHub API 호출
def get_issue_body():
    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    issue_body = response.json().get('body', '')
    return issue_body

# ChatGPT API 호출
def get_chatgpt_response(prompt):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

# 이슈에 댓글 추가
def comment_on_issue(comment):
    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": comment}
    requests.post(url, json=data, headers=headers)

def main():
    issue_body = get_issue_body()
    response = get_chatgpt_response(issue_body)
    comment_on_issue(response)

if __name__ == "__main__":
    main()
