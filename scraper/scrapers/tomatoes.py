from scraper.scrapers.base import BaseScraper
from scraper.models.movie import Movie, MovieLink

from typing import List, Dict, Optional


class Tomatoes(BaseScraper):
    __items_per_page__: int = 30
    __domain__: str = "https://www.rottentomatoes.com"

    def _retrieve_items_list(self, pages_count: int, genre: str) -> List[MovieLink]:
        movies: List[MovieLink] = []

        for page_num in range(1, pages_count):
            content = self._get_page_content(f"/browse/movies_at_home/genres:{genre}?page={page_num}")
            #print(content)
            #print(f"/browse/movies_at_home/genres:{genre}?page={page_num}") ###
            if content:
                #scraped_movie_divs = content.find_all('a', class_='js-tile-link')
                #print(scraped_movie_divs)
                #if not scraped_movie_divs:
                    #break  
                #print(content) 
                scraped_movie_titles = content.find_all('a', class_='js-tile-link')
                #print(scraped_movie_titles)                
                for i in range(len(scraped_movie_titles)):
                    if i + 1 < len(scraped_movie_titles):
                        title = scraped_movie_titles[i+1]
                        link = title['href']
                        #print(link) ###
                        movies.append(MovieLink(url=link))
                #print(movies) ###
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