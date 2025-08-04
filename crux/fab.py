import requests
from .config import FAB_API_URL, FAB_USER_ID, FAB_API_KEY

headers_fab = {
    "content-type": "application/json",
    "x-user-id": FAB_USER_ID,
    "x-authentication": f"api-key {FAB_API_KEY}"
}

def send_to_fab(file_path, code):
    codelines = '\n'.join(f"{i+1:3d}: {line}" for i, line in enumerate(code.split('\n')))
    payload = {
        "input": {
            "query": f"Please review this code:\n\nFile: {file_path}\n\n{codelines}\n\nProvide detailed code review analysis. Use the line numbers shown (e.g., '5: def function():' means line 5)."
        }
    }
    r = requests.post(FAB_API_URL, headers=headers_fab, json=payload)
    r.raise_for_status()
    return r.json().get("output", {}).get("content", str(r.json()))
