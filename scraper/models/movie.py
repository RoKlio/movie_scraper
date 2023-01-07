from pydantic import BaseModel
from typing import List


class Movie(BaseModel):
    title: str
    rating: str
    release_date: str
    description: str
    genre: List

class MovieLink(BaseModel):
    url: str