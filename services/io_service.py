import csv
import json
import os
from models.movie import Movie
from services.movie_service import MovieService
from services.director_service import DirectorService
from models.director import Director
class IOService:
    def __init__(self):
        self.movie_service = MovieService()
        self.director_service = DirectorService()
    def export_movies_to_csv(self, file_path):
        try:
            movies = self.movie_service.get_all_movies()
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Tiêu đề', 'Năm', 'Doanh thu', 'Đạo diễn ID'])
                for m in movies:
                    writer.writerow([m.id, m.title, m.year, m.revenue, m.director_id])
            return True
        except Exception as e:
            print(f"Lỗi xuất CSV: {e}")
            return False
    def export_movies_to_json(self, file_path):
        try:
            movies = self.movie_service.get_all_movies()
            # Chuyển đổi list object sang list dictionary
            data = [vars(m) for m in movies]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Lỗi xuất JSON: {e}")
            return False
    def _resolve_director_id(self, raw_id):
        if raw_id is not None and str(raw_id).strip().isdigit():
            d_id = int(raw_id)
            all_directors = self.director_service.get_all_directors()
            if any(d.id == d_id for d in all_directors):
                return d_id
        # tìm hoặc tạo đạo diễn tên "Unknown"
        all_directors = self.director_service.get_all_directors()
        unknown = next((d for d in all_directors if d.name == "Unknown"), None)
        if not unknown:
            unknown = self.director_service.add_director(
                Director(name="Unknown", birth_year=None)
            )
        return unknown.id
    def import_movies_from_csv(self, file_stream):
        try:
            # Đọc file CSV từ stream (tải lên từ trình duyệt)
            content = file_stream.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(content)
            # Kiểm tra các cột bắt buộc
            required = ['Tiêu đề', 'Năm', 'Doanh thu']
            if not all(col in reader.fieldnames for col in required):
                raise ValueError(f"File CSV thiếu các cột bắt buộc: {required}")
            count = 0
            for row in reader:
                try:
                    d_id = self._resolve_director_id(row.get('Đạo diễn ID'))
                    movie = Movie(
                        title=row['Tiêu đề'],
                        year=int(row['Năm']),
                        revenue=float(row['Doanh thu']),
                        director_id=d_id
                    )
                    self.movie_service.add_movie(movie)
                    count += 1
                except Exception as e:
                    print(f"Bỏ qua hàng lỗi: {e}")
            return count
        except Exception as e:
            raise Exception(f"Lỗi nhập CSV: {e}")
    def import_movies_from_json(self, file_stream):
        try:
            data = json.load(file_stream)
            if not isinstance(data, list):
                raise ValueError("JSON phải là một danh sách các phim.")
            count = 0
            for item in data:
                try:
                    d_id = self._resolve_director_id(item.get('director_id'))
                    movie = Movie(
                        title=item['title'],
                        year=int(item['year']),
                        revenue=float(item['revenue']),
                        director_id=d_id
                    )
                    self.movie_service.add_movie(movie)
                    count += 1
                except Exception as e:
                    print(f"Bỏ qua mục lỗi: {e}")
            return count
        except Exception as e:
            raise Exception(f"Lỗi nhập JSON: {e}")
