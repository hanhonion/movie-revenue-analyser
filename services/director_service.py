from models.director import Director
from repositories.director_repo import DirectorRepository
from repositories.movie_repo import MovieRepository
from datetime import datetime
 
class DirectorService:
    def __init__(self):
        self.repo = DirectorRepository()
        self.movie_repo = MovieRepository()
 
    def validate_director(self, director: Director):
        # Quy tắc 5.1: Tên đạo diễn không được trống
        if not director.name or not director.name.strip():
            raise ValueError("Tên đạo diễn không được để trống.")
        
        # Quy tắc 5.2: Năm sinh đạo diễn không được là tương lai
        if director.birth_year:
            current_year = datetime.now().year
            if director.birth_year > current_year:
                raise ValueError(f"Năm sinh đạo diễn ({director.birth_year}) không thể lớn hơn năm hiện tại ({current_year}).")
 
    def add_director(self, director: Director):
        self.validate_director(director)
        return self.repo.add(director)
 
    def update_director(self, director: Director):
        self.validate_director(director)
        return self.repo.update(director)
 
    def get_all_directors(self, search_query=None):
        return self.repo.get_all(search_query=search_query)
 
    def delete_director(self, director_id: int):
        # Quy tắc 4: Ràng buộc tham chiếu (Không xóa đạo diễn nếu còn phim)
        # Đây là quy tắc quan trọng trong quản lý DB
        movies = self.movie_repo.get_all()
        has_movies = any(m.director_id == director_id for m in movies)
        if has_movies:
            raise ValueError("LỖI NGHIỆP VỤ: Không thể xóa đạo diễn này vì họ đang có các bộ phim liên kết trong hệ thống. Hãy xóa phim của họ trước.")
        
        return self.repo.delete(director_id)
