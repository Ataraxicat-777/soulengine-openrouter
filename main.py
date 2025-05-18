import os
import json
import random
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
DATA_PATH = os.getenv("DATA_PATH", "soulengine_deployments.json")

# Initialize FastAPI app
app = FastAPI()

# --------- Middleware ---------
class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Pydantic Models ---------
class Message(BaseModel):
    message: str

class Construct(BaseModel):
    id: str
    name: str
    traits: list[str]
    score: float
    usd_value: float
    tier: str
    related_constructs: list[dict]

# --------- Helper Functions ---------
def get_constructs():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_constructs(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

# --------- API Routes ---------
@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

@app.get("/")
def root():
    return {"message": "SoulEngine backend is alive."}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SoulEngine API running."}

@app.get("/constructs")
def read_constructs():
    return get_constructs()

@app.post("/constructs")
def create_construct(construct: Construct):
    constructs = get_constructs()
    constructs.append(construct.dict())
    save_constructs(constructs)
    return construct

@app.post("/chat")
def chat(msg: Message):
    try:
        res = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are SoulEngine, an adaptive recursive construct."},
                {"role": "user", "content": msg.message}
            ]
        )
        return {"reply": res.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evolve")
def evolve(payload: dict):
    constructs = get_constructs()
    target_id = payload.get("id")
    found = next((c for c in constructs if c["id"] == target_id), None)
    if not found:
        raise HTTPException(status_code=404, detail="Construct not found")

    evolved = {
        **found,
        "id": f"{found['id']}_evolved",
        "traits": found["traits"] + ["mutated_trait"],
        "score": round(found["score"] + random.uniform(0.1, 1.0), 2)
    }
    constructs.append(evolved)
    save_constructs(constructs)
    return evolved

@app.post("/generate")
def generate_construct():
    new_id = f"construct_{random.randint(1000, 9999)}"
    construct = {
        "id": new_id,
        "name": f"Construct {new_id}",
        "traits": ["recursive", "harmonics", "adaptive"],
        "score": round(random.uniform(5.0, 10.0), 2),
        "usd_value": round(random.uniform(100, 500), 2),
        "tier": random.choice(["standard", "ultra", "legendary"]),
        "related_constructs": [],
    }
    constructs = get_constructs()
    constructs.append(construct)
    save_constructs(constructs)
    return construct