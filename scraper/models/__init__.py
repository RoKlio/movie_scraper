from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    rating: int
    release_date: str
    description: str
    earnings: int
