from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# --- NEW: This allows your Chrome Extension to talk to Python ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Extension + Browser)
    allow_methods=["*"],  # Allows all actions (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class EmailIn(BaseModel):
    sender: str
    body: str

class EmailOut(BaseModel):
    category: str
    priority: str
    summary: str

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/analyze", response_model=EmailOut)
def analyze_email(payload: EmailIn):
    # This is the "Dummy Logic" for your test
    return EmailOut(
        category="Work (Verified)",
        priority="High",
        summary=f"Mock summary for {payload.sender}"
    )