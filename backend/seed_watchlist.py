from database import SessionLocal, Base, engine
from models import Watchlist

Base.metadata.create_all(bind=engine)

db = SessionLocal()

entries = [
    ("xyz@company.com", "XYZ Team"),
    ("boss@office.com", "Manager"),
]

for email, category in entries:
    existing = db.query(Watchlist).filter(Watchlist.email == email).first()
    if not existing:
        db.add(Watchlist(email=email, category=category))

db.commit()
db.close()
