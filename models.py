from sqlalchemy import Column, Integer, String
from database import Base

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)