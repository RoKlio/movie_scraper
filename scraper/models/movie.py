from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    rating: str
    release_date: str
    description: str
    genre: str

class MovieLink(BaseModel):
    url: str