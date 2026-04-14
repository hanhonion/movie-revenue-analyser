from models.movie import Movie
from repositories.movie_repo import MovieRepository
from datetime import datetime

class MovieService:
    def __init__(self):
        self.repo = MovieRepository()

    def validate_movie(self, movie: Movie):
        # Quy tắc 1.1: Tên không để trống
        if not movie.title or not movie.title.strip():
            raise ValueError("Quy tắc: Tên phim không được để trống.")

        # Quy tắc 1.2: Doanh thu không được âm
        if movie.revenue < 0:
            raise ValueError(f"Quy tắc nghiệp vụ: Doanh thu (${movie.revenue}) không được phép là số âm.")

        # Quy tắc 2: Giới hạn năm phát hành
        current_year = datetime.now().year
        if movie.year < 1888 or movie.year > current_year + 5:
            raise ValueError(f"Quy tắc nghiệp vụ: Năm phát hành ({movie.year}) phải nằm trong khoảng từ 1888 đến {current_year + 5}.")

        # Quy tắc 3: Chống trùng lặp (Phim đã tồn tại)
        existing = self.repo.find_by_title_and_year(movie.title, movie.year)
        if existing and (movie.id is None or existing.id != movie.id):
            raise ValueError(f"Quy tắc nghiệp vụ: Phim '{movie.title}' sản xuất năm {movie.year} đã tồn tại trong hệ thống. Không được phép thêm trùng.")

    def add_movie(self, movie: Movie):
        self.validate_movie(movie)
        return self.repo.add(movie)

    def update_movie(self, movie: Movie):
        self.validate_movie(movie)
        return self.repo.update(movie)

    def delete_movie(self, movie_id: int):
        return self.repo.delete(movie_id)

    def get_all_movies(self, search_query=None, sort_by=None, director_id=None):
        return self.repo.get_all(search_query=search_query, sort_by=sort_by, director_id=director_id)

    def get_statistics(self, search_query=None, sort_by=None, director_id=None):
        movies = self.repo.get_all(search_query=search_query, sort_by=sort_by, director_id=director_id)
        if not movies:
            return {"count": 0, "total_revenue": 0, "avg_revenue": 0, "top_movies": []}
        
        total_rev = sum(m.revenue for m in movies)
        avg_rev = total_rev / len(movies)
        top_movies = sorted(movies, key=lambda x: x.revenue, reverse=True)[:5]
        
        return {
            "count": len(movies),
            "total_revenue": round(total_rev, 2),
            "avg_revenue": round(avg_rev, 2),
            "top_movies": top_movies
        }

    def get_movie_by_id(self, movie_id: int):
        return self.repo.get_by_id(movie_id)
