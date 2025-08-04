
import requests
import base64
from .config import GITHUB_PAT

headers = {
    "Authorization": f"Bearer {GITHUB_PAT}",
    "Accept": "application/vnd.github+json"
}

def get_open_prs(repo):
    url = f"https://api.github.com/repos/{repo}/pulls?state=open"
    return requests.get(url, headers=headers).json()

def get_pr_files(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    return requests.get(url, headers=headers).json()

def get_file_content(repo, path, ref):
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return base64.b64decode(r.json().get("content", "")).decode()
    return None

def post_review_comment(repo, pr_number, path, line, message, commit_id):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
    payload = {
        "body": message,
        "commit_id": commit_id,
        "path": path,
        "line": line,
        "side": "RIGHT"
    }
    return requests.post(url, headers=headers, json=payload)
