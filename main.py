import os
import jwt
import time
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header
from crux.reviewer import review

load_dotenv('credentials.env')

APP_ID = os.getenv("APP_ID")
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

app = FastAPI()

def generate_jwt():
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": APP_ID
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def get_installation_token(installation_id):
    jwt_token = generate_jwt()
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    res = requests.post(url, headers=headers)
    res.raise_for_status()
    return res.json()["token"]

@app.post("/webhook")
async def handle_webhook(request: Request, x_github_event: str = Header(None)):
    payload = await request.json()

    if x_github_event == "pull_request":
        action = payload["action"]
        if action in ["opened", "reopened", "synchronize"]:
            repo = payload["repository"]["full_name"]
            pr_number = payload["pull_request"]["number"]
            head_sha = payload["pull_request"]["head"]["sha"]
            installation_id = payload["installation"]["id"]

            print(f"\n PR Event: #{pr_number} in {repo} — {action}")
            token = get_installation_token(installation_id)
            review(repo,pr_number,head_sha,token)

    return {"status": "ok"}
