from abc import ABC, abstractmethod
from typing import List

from scraper.models.movie import MovieLink, Movie

class BaseScraper(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def _retrieve_items_list(self) -> List[MovieLink]:
        pass

    def scrape(self, movie_count: int, genre: str) -> List[Movie]:
        pass
