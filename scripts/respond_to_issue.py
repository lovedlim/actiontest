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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# 이슈에 댓글 추가
def comment_on_issue(comment):
    if not comment:
        print("No comment to post.")
        return

    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": comment}
    response = requests.post(url, json=data, headers=headers)
    
    # 응답 상태 코드와 메시지 출력
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print(f"Failed to post comment. Status code: {response.status_code}, Response: {response.text}")

def main():
    issue_body = get_issue_body()
    if issue_body:  # 이슈 내용이 있을 때만 응답 생성
        response = get_chatgpt_response(issue_body)
        print(f"Generated response: {response}")  # 디버깅용 출력
        comment_on_issue(response)
    else:
        print("No issue body found.")

if __name__ == "__main__":
    main()

# import os
# import openai
# import requests

# # GitHub 환경 변수 설정
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
# REPO_NAME = os.getenv('GITHUB_REPOSITORY')
# ISSUE_NUMBER = os.getenv('ISSUE_NUMBER')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# # OpenAI API 키 설정
# openai.api_key = OPENAI_API_KEY

# # 이슈의 내용을 가져오기 위해 GitHub API 호출
# def get_issue_body():
#     url = f"https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}"
#     headers = {"Authorization": f"token {GITHUB_TOKEN}"}
#     response = requests.get(url, headers=headers)
#     issue_body = response.json().get('body', '')
#     return issue_body

# # ChatGPT API 호출
# def get_chatgpt_response(prompt):
#     response = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",  # 최신 모델명으로 업데이트
#       messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#       ],
#       max_tokens=150
#     )
#     return response.choices[0].message['content'].strip()

# # 이슈에 댓글 추가
# def comment_on_issue(comment):
#     url = f"https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}/comments"
#     headers = {"Authorization": f"token {GITHUB_TOKEN}"}
#     data = {"body": comment}
#     requests.post(url, json=data, headers=headers)

# def main():
#     issue_body = get_issue_body()
#     if issue_body:  # 이슈 내용이 있을 때만 응답 생성
#         response = get_chatgpt_response(issue_body)
#         comment_on_issue(response)
#     else:
#         print("No issue body found.")

# if __name__ == "__main__":
#     main()
