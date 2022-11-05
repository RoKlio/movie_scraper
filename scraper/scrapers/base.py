from abc import ABC, abstractmethod
from typing import List, Optional
import math
import requests
from bs4 import BeautifulSoup

from scraper.models.movie import MovieLink, Movie

class BaseScraper(ABC):
    __items_per_page__: int = 50
    __domain__: str = ""

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, genre: str) -> List[MovieLink]:
        pass
    
    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content)
        raise Exception("Cannot reach content!")

    @abstractmethod
    def _retrieve_movie_info(self, link: MovieLink) -> Optional[Movie]:
        pass

    def scrape(self, movies_count: int, genre: str) -> List[Movie]:
        try:
            pages_count = math.ceil(movies_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise AttributeError("Movies per page is set to 0!")
        movies_links = self._retrieve_items_list(pages_count, genre)
        scraped_movies = [self._retrieve_movie_info(movie_link) for movie_link in movies_links]
        return [scraped_movie for scraped_movie in scraped_movies if scraped_movie is not None]
