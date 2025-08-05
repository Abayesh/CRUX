import requests
from crux.config import FAB_API_URL, FAB_API_KEY, FAB_USER_ID

headers_fab = {
    "content-type": "application/json",
    "x-user-id": FAB_USER_ID,
    "x-authentication": f"api-key {FAB_API_KEY}"
}

def get_fab_review(file_path, code):
    lines = code.split('\n')
    codelines = []
    for i, line in enumerate(lines):
        codelines.append(f"{i+1:3d}: {line}")
    codes = '\n'.join(codelines)
    payload = {
        "input": {
            "query": f"Please review this code:\n\nFile: {file_path}\n\n{codes}\n\nProvide detailed code review analysis. Use the line numbers shown."
        }
    }
    response = requests.post(FAB_API_URL, headers=headers_fab, json=payload)
    response.raise_for_status()
    return response.json()['output']['content']
