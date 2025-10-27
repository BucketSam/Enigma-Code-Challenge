from pydantic import BaseModel
from datetime import date
from typing import Optional

class Book(BaseModel):
    id: Optional[int] = None 
    title: str
    author: str
    published_date: Optional[date] = None
    isbn: str

