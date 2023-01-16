from scraper.scrapers.base import BaseScraper
from scraper.models.movie import Movie, MovieLink

from typing import List, Dict, Optional


class Imdb(BaseScraper):
    __items_per_page__: int = 50
    __domain__: str = "https://www.imdb.com"

    def _retrieve_items_list(self, pages_count: int, genre: str) -> List[MovieLink]:
        movies: List[MovieLink] = []

        for page_num in range(0, pages_count):
            content = self._get_page_content(f"/search/title/?title_type=feature&genres={genre}&start={page_num*50+1}&ref_=adv_nxt")
            #print(pages_count)
            #print(f"/search/title/?title_type=feature&genres={genre}&start={page_num*50+1}&ref_=adv_nxt")
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
                #title_years = content.find('h3', class_='lister-item-header')
                #movie_title = title_years.find('a').text
                #movie_title = movie_title.replace('\n', '').strip()
                #release_date = title_years.find('span', class_='lister-item-year text-muted unbold').text
                title = content.find_all('div')[76].find('h1').text
                genre = content.find_all('div')[137].text
                #genre = genre.replace('\n', '').strip()
                description = content.find_all('div')[134].find_all('span')[4].text
                rating = content.find_all('div')[602].text
                release_date = content.find_all('div')[678].text
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

