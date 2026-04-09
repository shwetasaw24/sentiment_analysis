# app/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas, auth, sentiment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 REGISTER
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = auth.hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}


# 🔐 LOGIN
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(email=user.email).first()
    
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_token({"user_id": db_user.id})
    return {"token": token}


# 📦 GET PRODUCTS (NOT PROTECTED)
@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    print("DEBUG:", products)
    return products


# 📝 SUBMIT FEEDBACK
@router.post("/feedback")
def submit_feedback(
    data: schemas.FeedbackCreate,
    user_id: int = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    result = sentiment.predict_sentiment(data.text)

    feedback = models.Feedback(
        user_id=user_id,
        product=data.product,
        text=data.text,
        positive_prob=result["positive"],
        negative_prob=result["negative"],
        sentiment=result["label"]
    )

    db.add(feedback)
    db.commit()

    return {"analysis": result}


# 📊 GET FEEDBACK
@router.get("/feedback")
def get_feedback(
    user_id: int = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    feedbacks = db.query(models.Feedback).filter_by(user_id=user_id).all()
    return [schemas.FeedbackResponse.from_orm(f) for f in feedbacks]


# 📊 GET SENTIMENT STATS
@router.get("/sentiment/stats")
def get_sentiment_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    stats = db.query(
        models.Feedback.product,
        func.avg(models.Feedback.positive_prob).label('avg_positive'),
        func.avg(models.Feedback.negative_prob).label('avg_negative'),
        func.count(models.Feedback.id).label('count')
    ).group_by(models.Feedback.product).all()
    
    return [
        {
            "product": s.product,
            "avg_positive": float(s.avg_positive),
            "avg_negative": float(s.avg_negative),
            "count": s.count
        }
        for s in stats
    ]


# 📊 PRODUCT SUMMARY
@router.get("/product/{product_name}")
def product_summary(
    product_name: str,
    user_id: int = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    feedbacks = db.query(models.Feedback).filter(
        models.Feedback.product == product_name
    ).all()

    total = len(feedbacks)
    pos = sum(1 for f in feedbacks if f.sentiment == "POSITIVE")

    if total == 0:
        return {"message": "No data"}

    return {
        "rating": round((pos / total) * 5, 2),
        "total_reviews": total
    }