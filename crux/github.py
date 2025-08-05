import requests
import base64

def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_file_content(repo, file_path, ref, token):
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={ref}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json().get("content", "")
        return base64.b64decode(content).decode()
    return None

def post_comment(repo, pr_number, path, line, message, commit_id, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    payload = {
        "body": message,
        "commit_id": commit_id,
        "path": path,
        "line": line,
        "side": "RIGHT"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        print(f" Failed to post comment: {response.status_code} - {response.text}")
