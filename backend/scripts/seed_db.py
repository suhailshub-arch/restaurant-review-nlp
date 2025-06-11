# backend/scripts/seed_db.py

import os
import json
from sqlalchemy.orm import Session
from app.db import engine, SessionLocal
from app.models import Base, Restaurant, Review

def load_data():
    """Load seed data from JSON file next to this script."""
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "seed_data.json")) as f:
        return json.load(f)

def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    data = load_data()
    db: Session = SessionLocal()
    try:
        # Seed restaurants
        for r in data["restaurants"]:
            db.merge(Restaurant(**r))   # merge = insert or update
        db.commit()

        # Optionally seed reviews
        for rv in data.get("reviews", []):
            db.merge(Review(**rv))
        db.commit()

        print("✅ Database seeded successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
