from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas, auth, sentiment

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed = auth.hash_password(user.password)
    
    new_user = models.User(email=user.email, password=hashed)
    
    db.add(new_user)
    db.commit()
    
    return {"message": "User created"}

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not db_user or not auth.verify_password(user.password, db_user.password):
        return {"error": "Invalid credentials"}
    
    token = auth.create_token({"user_id": db_user.id})
    
    return {"token": token}

@router.post("/feedback")
def submit_feedback(data: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    
    result = sentiment.predict_sentiment(data.text)
    
    feedback = models.Feedback(
        user_id=1,  # simplify for now
        product=data.product,
        text=data.text,
        positive_prob=result["positive"],
        negative_prob=result["negative"],
        sentiment=result["label"]
    )
    
    db.add(feedback)
    db.commit()
    
    return {
        "message": "Stored",
        "analysis": result
    }

@router.get("/product/{product_name}")
def product_summary(product_name: str, db: Session = Depends(get_db)):
    
    feedbacks = db.query(models.Feedback).filter(
        models.Feedback.product == product_name
    ).all()
    
    total = len(feedbacks)
    pos = sum(1 for f in feedbacks if f.sentiment == "POSITIVE")
    
    if total == 0:
        return {"message": "No data"}
    
    rating = (pos / total) * 5
    
    return {
        "product": product_name,
        "rating": round(rating, 2),
        "total_reviews": total,
        "positive_ratio": pos / total
    }

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()