import films

from database import Base, engine
from router import router
from schemas import Film, FilmCreate

from fastapi import FastAPI, HTTPException

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from models import Film

import uvicorn

DATABASE_URL = "sqlite:///./test1.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

if __name__ == "__main__": uvicorn.run(app)