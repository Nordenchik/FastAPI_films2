from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 💾 Налаштування бази даних
DATABASE_URL = "sqlite:///./test1.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# 👤 Модель фільму
class Film(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# 🧱 Створення таблиць
def init_db(): Base.metadata.create_all(bind=engine)

# 🔄 Отримання сесії (ручна альтернатива get_db)
def get_session() -> Session: return SessionLocal()

# ➕ Створити фільм
def create_film(name: str):
    db = get_session()
    film = Film(name=name)
    db.add(film)
    db.commit()
    db.refresh(film)
    db.close()
    #print(f"[+] Створено фільм:  - {film.name}")

# 📋 Отримати всі фільми
def list_films():
    db = get_session()
    films = db.query(Film).all()
    db.close()
    print("[📋] Всі фільми:")
    for film in films: print(f"{film.id}: {film.name}")

# 🔍 Знайти фільм за назвою
def find_film(name: str):
    db = get_session()
    film = db.query(Film).filter(Film.name == name).first()
    db.close()
    if film: print(f"[🔍] Знайдено: {film.id} - {film.name}")
    else: print("[❌] Фільм не знайдено")

# ✏️ Оновити назву фільма
def update_film(film_id: int, new_name: str):
    db = get_session()
    film = db.query(Film).filter(Film.id == film_id).first()
    if film:
        film.name = new_name
        db.commit()
        print(f"[✏️] Оновлено: ID {film_id} → {new_name}")
    else: print("[❌] Фільм не знайдено")
    db.close()

# ❌ Видалити фільм
def delete_film(film_id: int):
    db = get_session()
    film = db.query(Film).filter(Film.id == film_id).first()
    if film:
        db.delete(film)
        db.commit()
        print(f"[🗑️] Фільм видалено з ID {film_id}")
    else: print("[❌] Фільм не знайдено")
    db.close()

# 🧪 Демонстрація роботи
if __name__ == "__main__":
    #Base.metadata.create_all(bind=engine)

    #create_film("Alice2")
    #create_film("Bob")

    #list_films()

    #find_film("Alice")

    #update_film(1, "Backrooms")

    delete_film(2)

    # list_films()