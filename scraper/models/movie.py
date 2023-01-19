from pydantic import BaseModel
from typing import List


class Movie(BaseModel):
    title: str
    rating: str
    release_date: str
    description: str
    genre: List
    critics_score: str
    top_actors: List
    producer: str

class MovieLink(BaseModel):
    url: str