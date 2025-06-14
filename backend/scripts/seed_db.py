# backend/scripts/seed_db.py

import os
import json
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import engine, SessionLocal
from app.models import Restaurant, Review

def load_data():
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "seed_data.json")) as f:
        return json.load(f)

def seed():

    data = load_data()
    db: Session = SessionLocal()
    try:
        # 2) Upsert restaurants
        for r in data["restaurants"]:
            db.merge(Restaurant(**r))
        db.commit()

        # 3) Upsert reviews
        for rv in data.get("reviews", []):
            db.merge(Review(**rv))
        db.commit()

        # 4) Reset the restaurants_id_seq
        db.execute(text("""
            SELECT setval(
                pg_get_serial_sequence('restaurants','id'),
                (SELECT COALESCE(MAX(id), 0) FROM restaurants) + 1,
                false
            );
        """))
        # 5) Reset the reviews_id_seq (if you seeded explicit IDs there too)
        db.execute(text("""
            SELECT setval(
                pg_get_serial_sequence('reviews','id'),
                (SELECT COALESCE(MAX(id), 0) FROM reviews) + 1,
                false
            );
        """))
        db.commit()

        print("✅ Database seeded and sequences reset.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
