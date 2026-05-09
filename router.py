from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from database import get_db
from models import Film
from schemas import FilmCreate, FilmRead, FilmUpdate

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def films_page(request: Request, db: Session = Depends(get_db)):
    films = db.query(Film).order_by(Film.id).all()
    return templates.TemplateResponse(request=request, name="films.html", context={"request": request, "films": films})

@router.post("/films/create")
def create_film_form(name: str = Form(...), price: float = Form(...), db: Session = Depends(get_db)):
    film = Film(name=name, price=price)
    db.add(film)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.put("/films/{film_id}/update")
def update_film_form(film_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film: raise HTTPException(status_code=404, detail="Фільм не знайдено")
    film.name = name
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.delete("/films/{film_id}/delete")
def delete_film_form(film_id: int, db: Session = Depends(get_db)):
    film = db.query(film).filter(film.id == film_id).first()
    if not film: raise HTTPException(status_code=404, detail="Фільм не знайдено")
    db.delete(film)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/api/films", response_model=list[FilmRead])
def read_films(db: Session = Depends(get_db)):
    return db.query(Film).order_by(Film.id).all()

@router.get("/api/films/{film_id}", response_model=FilmRead)
def read_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(film).filter(film.id == film_id).first()
    if not film: raise HTTPException(status_code=404, detail="Фільм не знайдено")
    return film

@router.post("/api/films", response_model=FilmRead)
def create_film(film: FilmCreate, db: Session = Depends(get_db)):
    db_film = film(name=film.name)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film

@router.put("/api/films/{film_id}", response_model=FilmRead)
def update_film(film_id: int, payload: FilmUpdate, db: Session = Depends(get_db)):
    film = db.query(film).filter(film.id == film_id).first()
    if not film: raise HTTPException(status_code=404, detail="Фільм не знайдено")
    film.name = payload.name
    db.commit()
    db.refresh(film)
    return film

@router.delete("/api/films/{film_id}")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(film).filter(film.id == film_id).first()
    if not film: raise HTTPException(status_code=404, detail="Фільм не знайдено")
    db.delete(film)
    db.commit()
    return {"status": "deleted"}