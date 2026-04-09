# seed.py

from database import SessionLocal
from models import Product

db = SessionLocal()

products = [
    {"name": "iPhone 15", "description": "Apple smartphone"},
    {"name": "Samsung S23", "description": "Samsung flagship"},
    {"name": "MacBook Air", "description": "Lightweight laptop"},
    {"name": "Boat Headphones", "description": "Affordable audio device"}
]

for p in products:
    exists = db.query(Product).filter_by(name=p["name"]).first()
    if not exists:
        db.add(Product(**p))

db.commit()
db.close()

print("✅ Products inserted successfully!")