from scraper.scrapers.base import BaseScraper
from scraper.models.movie import Movie, MovieLink

from typing import List, Dict, Optional

from bs4 import BeautifulSoup
import requests
import pandas as pd


class Imdb(BaseScraper):
    __items_per_page_: int = 50
    __domain__: str = "https://www.imdb.com"

    def _retrieve_items_list(self, pages_count: int, genre: str) -> List[MovieLink]:
        movies: List[MovieLink] = []
        
        for page_num in range(pages_count):
            content = self._get_page_content(f"/search/title/?groups=top_250&sort=user_rating/desc&start={page_num*50+1}&ref_=adv_prv")
            if content:
                scraped_movie_divs = content.find('div', class_='lister-list')
                if not scraped_movie_divs:
                    break   
                scraped_movie_titles = scraped_movie_divs.find_all('div', class_='lister-item mode-advanced')                
                for movie in scraped_movie_titles:
                    link = movie.find('a')['href']
                    movies.append(MovieLink(url=link))
            else:
                continue
        return movies

    
    def _retrieve_movie_info(self, link: MovieLink) -> Optional[Movie]:
        content = self._get_page_content(link.url)
        if content:
            try:
                title_years = content.find('h3', class_='lister-item-header')
                title = title_years.find('a').text
                title = title.replace('\n', '').strip()
                release_date = title_years.find('span', class_='lister-item-year text-muted unbold').text
                genre = content.find('span', class_='genre').text
                genre = genre.replace('\n', '').strip()
                description = movie.find_all('p', class_='text-muted')[1].text.strip()
                rating = content.find('div', class_='inline-block ratings-imdb-rating').text.strip()
                link = content.find('a')['href']
        else:
            return None

            scraped_movie_divs = soup.find('div', class_='lister-list')

