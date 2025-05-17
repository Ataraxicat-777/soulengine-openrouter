from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import os
from datetime import datetime

app = FastAPI(title="SoulEngine API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = "soulengine_log.json"
DEPLOY_FILE = "soulengine_deployments.json"
RENDER_FILE = "render_ready.json"

class Construct(BaseModel):
    id: str
    name: str
    score: float
    usd_value: Optional[float] = None
    traits: List[str]
    description: str
    tier: str
    aliases: List[str] = []
    evolved_from: List[str] = []
    timestamp: Optional[str] = None
    trait_info: List[str] = []

@app.on_event("startup")
def ensure_files():
    for file_path in [LOG_FILE, DEPLOY_FILE, RENDER_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

@app.get("/constructs", response_model=List[Construct])
def list_constructs():
    try:
        with open(DEPLOY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading deployments: {e}")

@app.post("/constructs", response_model=Construct)
def add_construct(construct: Construct):
    construct.id = construct.id or str(uuid.uuid4())
    construct.timestamp = datetime.utcnow().isoformat()
    construct.usd_value = round(construct.score * 42.0, 2)

    try:
        with open(DEPLOY_FILE, "r+") as f:
            data = json.load(f)
            data.append(construct.dict())
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        return construct
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save construct: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SoulEngine API running."}