from pydantic import BaseModel, Field

class Film(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    price: float = Field(..., gt=50)

class FilmCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Назва фільму")
    price: str = Field(..., min_length=2, description="Ціна білету на фільм")

class FilmRead(BaseModel):
    id: int
    class Config: from_attributes: True

class FilmUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Назва фільму")
    price: str = Field(..., min_length=2, description="Ціна білету на фільм")