# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import router
from app import models  # 🔥 IMPORTANT
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ ROUTES
app.include_router(router)