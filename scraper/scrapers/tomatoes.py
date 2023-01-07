from scraper.scrapers.base import BaseScraper
from scraper.models.movie import Movie, MovieLink

from typing import List, Dict, Optional


class Tomatoes(BaseScraper):
    __items_per_page__: int = 30
    __domain__: str = "https://www.rottentomatoes.com"

    def _retrieve_items_list(self, pages_count: int, genre: str) -> List[MovieLink]:
        movies: List[MovieLink] = []

        for page_num in range(0, pages_count):
            content = self._get_page_content(f"/browse/movies_at_home/genres:{genre}?page={page_num}")
            #print(pages_count)
            #print(f"/search/title/?title_type=feature&genres={genre}&start={page_num*50+1}&ref_=adv_nxt")
            if content:
                scraped_movie_divs = content.find('div', class_='discovery-tiles')
                if not scraped_movie_divs:
                    break   
                scraped_movie_titles = scraped_movie_divs.find_all('div', class_='js-title-link')                
                for movie in scraped_movie_titles:
                    link = movie.find('a')['href']
                    movies.append(MovieLink(url=link))
            else:
                continue
        return movies

    
    def _retrieve_movie_info(self, link: MovieLink) -> Optional[Movie]:
        content = self._get_page_content(link.url)
        if content:
                title = content.find('h1', class_='scoreboard__title').text.strip()
                genre = content.find('div', class_='meta-value genre').text.split()
                description = content.find('div', id='movieSynopsis').text.strip()
                rating = content.find('score-board')['audiencescore']
                release_date = content.find('time').text
                #link = content.find('a')['href']
                return Movie(
                    title=title,
                    rating=rating,
                    release_date=release_date,
                    description=description,
                    genre=genre
                    )
        else:
            return None