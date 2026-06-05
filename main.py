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

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.include_router(router)

if __name__ == "__main__": uvicorn.run(app)