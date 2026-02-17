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
# Change 'request: Request' to 'payload: GithubPayload'
async def handle_github_event(payload: GithubPayload, x_hub_signature_256: str = Header(None)):
    
    # You no longer need: payload = await request.json()
    # FastAPI handles that automatically now!
    
    commit_msg = payload.head_commit.get("message", "") if payload.head_commit else ""

    if "deploy" in commit_msg:
        async with httpx.AsyncClient() as client:
            # Send the payload directly
            response = await client.post(N8N_WEBHOOK_URL, json=payload.model_dump())
            return {"status": "n8n triggered", "n8n_response": response.status_code}

    return {"status": "skipped", "reason": "No deploy keyword"}
