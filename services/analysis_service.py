import matplotlib
matplotlib.use('Agg') # Ngăn lỗi 'main thread is not in main loop' trên Flask
import matplotlib.pyplot as plt
import io
import base64
from repositories.movie_repo import MovieRepository

class AnalysisService:
    def __init__(self):
        self.movie_repo = MovieRepository()

    def get_statistics(self, search_query=None, sort_by=None, director_id=None):
        movies = self.movie_repo.get_all(search_query=search_query, sort_by=sort_by, director_id=director_id)
        if not movies:
            return {"count": 0, "total_revenue": 0, "avg_revenue": 0, "top_movies": []}
            
        total_rev = sum(m.revenue for m in movies)
        avg_rev = total_rev / len(movies)
        # Sắp xếp theo doanh thu giảm dần để lấy Top 5
        top_movies = sorted(movies, key=lambda x: x.revenue, reverse=True)[:5]
        
        return {
            "count": len(movies),
            "total_revenue": round(total_rev, 2),
            "avg_revenue": round(avg_rev, 2),
            "top_movies": top_movies
        }

    def generate_charts(self):
        movies = self.movie_repo.get_all()
        if not movies:
            return None

        # 1. Thống kê theo thời gian (Gộp doanh thu theo từng năm)
        year_data = {}
        for m in movies:
            year_data[m.year] = year_data.get(m.year, 0) + m.revenue
        
        sorted_years = sorted(year_data.keys())
        total_revenues_m = [year_data[y] / 1_000_000 for y in sorted_years] # Đơn vị: Triệu USD

        # 2. Chuẩn bị vẽ 2 biểu đồ (Subplots)
        plt.style.use('ggplot')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # Biểu đồ 1: Xu hướng doanh thu theo năm (Line Chart)
        ax1.plot(sorted_years, total_revenues_m, marker='o', color='#28a745', linewidth=2)
        ax1.set_title('Xu hướng Tổng doanh thu theo Năm', fontsize=14, pad=15)
        ax1.set_xlabel('Năm')
        ax1.set_ylabel('Tổng doanh thu (Triệu $)')
        ax1.grid(True, alpha=0.3)

        # Biểu đồ 2: Top 5 phim doanh thu cao nhất (Bar Chart)
        top_5 = sorted(movies, key=lambda x: x.revenue, reverse=True)[:5]
        titles = [m.title[:15] + "..." if len(m.title) > 15 else m.title for m in top_5]
        revs = [m.revenue / 1_000_000 for m in top_5]
        
        ax2.bar(titles, revs, color=['#ffc107', '#17a2b8', '#dc3545', '#007bff', '#6610f2'])
        ax2.set_title('Top 5 Phim có Doanh thu cao nhất', fontsize=14, pad=15)
        ax2.set_ylabel('Doanh thu (Triệu $)')
        
        plt.tight_layout()
        
        # Chuyển đổi sang Base64 để hiển thị trên Web
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return chart_base64
