from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import Watchlist, EmailLog

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS for extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Pydantic models ----------

class EmailIn(BaseModel):
    sender: str
    body: str


class EmailOut(BaseModel):
    category: str
    priority: str
    summary: str


class EmailLogOut(BaseModel):
    id: int
    sender: str
    body: str
    category: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2


# ---------- DB session dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Routes ----------

@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/analyze", response_model=EmailOut)
def analyze_email(payload: EmailIn, db: Session = Depends(get_db)):
    # 1) Watchlist check
    wl = db.query(Watchlist).filter(Watchlist.email == payload.sender).first()

    if wl:
        category = wl.category
        priority = "High"
    else:
        category = "General"
        priority = "Normal"

    summary = f"Mock summary for {payload.sender}"

    # 2) Save log into database
    log = EmailLog(
        sender=payload.sender,
        body=payload.body,
        category=category,
        priority=priority,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return EmailOut(
        category=category,
        priority=priority,
        summary=summary,
    )


@app.get("/list_emails", response_model=List[EmailLogOut])
def list_emails(limit: int = 20, db: Session = Depends(get_db)):
    logs = (
        db.query(EmailLog)
        .order_by(EmailLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return logs
