import requests
from bs4 import BeautifulSoup
import re
import time
from models.movie import Movie
from models.director import Director
from services.movie_service import MovieService
from services.director_service import DirectorService

class CrawlerService:
    def __init__(self):
        self.movie_service = MovieService()
        self.director_service = DirectorService()
        self.base_url = "https://en.wikipedia.org"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def _get_director_birth_year(self, director_url):
        """Truy cập trang cá nhân của đạo diễn để lấy năm sinh"""
        if not director_url: return None
        try:
            res = requests.get(self.base_url + director_url, headers=self.headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            # Thường nằm trong class 'bday' (ISO format) hoặc mục Born
            bday = soup.find(class_='bday')
            if bday:
                year_match = re.search(r'\d{4}', bday.text)
                if year_match: return int(year_match.group())
            
            # Nếu không có thẻ bday, tìm trong bảng Infobox
            infobox = soup.find('table', {'class': 'infobox'})
            if infobox:
                for tr in infobox.find_all('tr'):
                    th = tr.find('th')
                    if th and "Born" in th.text:
                        td = tr.find('td')
                        if td:
                            year_match = re.search(r'\d{4}', td.text)
                            if year_match: return int(year_match.group())
            return None
        except Exception:
            return None

    def _get_director_info_from_movie_page(self, movie_url):
        """Lấy tên và URL của Đạo diễn từ trang phim"""
        try:
            res = requests.get(self.base_url + movie_url, headers=self.headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            infobox = soup.find('table', {'class': 'infobox'})
            if not infobox: return "Unknown Director", None
            
            for tr in infobox.find_all('tr'):
                th = tr.find('th')
                if th and "Directed by" in th.text:
                    td = tr.find('td')
                    if td:
                        link = td.find('a')
                        name = td.text.strip().split('\n')[0].split(',')[0]
                        url = link.get('href') if link else None
                        return name, url
            return "Unknown Director", None
        except Exception:
            return "Unknown Director", None

    def crawl_movies(self, limit=50):
        url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
        count = 0
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = soup.find('table', {'class': 'wikitable'})
            if not table: return self.seed_initial_data()

            rows = table.find_all('tr')[1:] 
            
            for row in rows[:limit+10]: 
                if count >= limit: break
                try:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) < 5: continue
                    
                    title_cell = cols[2]
                    title_link = title_cell.find('a')
                    title = title_link.text.strip() if title_link else title_cell.text.strip()
                    title = re.sub(r'[†\*]|\s*\[.*\]', '', title).strip()
                    
                    movie_url = title_link.get('href') if title_link else None
                    
                    gross_text = cols[3].text.strip()
                    gross_match = re.search(r'\$[\d,]+', gross_text)
                    revenue = float(gross_match.group().replace('$', '').replace(',', '')) if gross_match else 0.0
                        
                    year_match = re.search(r'\d{4}', cols[4].text.strip())
                    year = int(year_match.group()) if year_match else 2024
                    
                    # QUY TRÌNH MỚI: Lấy cả thông tin năm sinh đạo diễn
                    director_name = "Unknown"
                    birth_year = None
                    if movie_url:
                        print(f"Đang phân tích phim: {title}...")
                        director_name, director_url = self._get_director_info_from_movie_page(movie_url)
                        if director_url:
                            print(f"  -> Đang tìm năm sinh đạo diễn {director_name}...")
                            birth_year = self._get_director_birth_year(director_url)
                            time.sleep(0.3) 
                    
                    # Lưu Đạo diễn và Năm sinh
                    directors = self.director_service.get_all_directors()
                    target_dir = next((d for d in directors if d.name == director_name), None)
                    if not target_dir:
                        target_dir = self.director_service.add_director(Director(name=director_name, birth_year=birth_year))
                    elif birth_year and target_dir.birth_year != birth_year:
                        # Cập nhật năm sinh nếu trước đó chưa có
                        target_dir.birth_year = birth_year
                        self.director_service.repo.update(target_dir)
                    
                    self.movie_service.add_movie(Movie(title=title, year=year, revenue=revenue, director_id=target_dir.id))
                    count += 1
                except Exception as e:
                    print(f"Bỏ qua dòng lỗi: {e}")
                    continue
            
            return count if count > 0 else self.seed_initial_data()

        except Exception as e:
            print(f"Lỗi Wikipedia: {e}")
            return self.seed_initial_data()

    def seed_initial_data(self):
        sample_movies = [
            ("Avatar", 2009, 2923706026.0, "James Cameron", 1954),
            ("Avengers: Endgame", 2019, 2797501328.0, "Anthony Russo", 1970),
            ("Titanic", 1997, 2257844554.0, "James Cameron", 1954)
        ]
        count = 0
        for title, year, rev, d_name, d_year in sample_movies:
            # Logic check existing and add...
            pass
        return count
