from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class GithubPayload(BaseModel):
    head_commit: dict = None
    pusher: dict = None
    repository: dict = None
# Configuration (Use Environment Variables for security)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://jorgette.tail3679cb.ts.net/webhook-test/github-trigger")
SECRET_TOKEN = os.getenv("GITHUB_TO_FASTAPI_SECRET")

@app.post("/github-event")
async def handle_github_event(request: Request, x_hub_signature_256: str = Header(None)):
    # 1. (Optional) Validate GitHub Signature for security
    payload = await request.json()
    
    # 2. Add custom logic: e.g., only trigger n8n if the commit message contains 'deploy'
    commit_msg = payload.get("head_commit", {}).get("message", "")
    
    if "deploy" in commit_msg:
        async with httpx.AsyncClient() as client:
            # 3. Forward to n8n Webhook
            response = await client.post(N8N_WEBHOOK_URL, json=payload)
            return {"status": "n8n triggered", "n8n_response": response.status_code}
    
    return {"status": "skipped", "reason": "No deploy keyword"}
