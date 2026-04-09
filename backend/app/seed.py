from app.database import SessionLocal
from app import models

db = SessionLocal()

products = [
    {"name": "iPhone 15", "description": "Apple smartphone"},
    {"name": "Samsung S23", "description": "Samsung flagship phone"},
    {"name": "Boat Headphones", "description": "Affordable audio gear"},
    {"name": "MacBook Air", "description": "Apple lightweight laptop"}
]

for p in products:
    existing = db.query(models.Product).filter_by(name=p["name"]).first()
    if not existing:
        db.add(models.Product(**p))

db.commit()
print("Products added!")