from flask import Flask, render_template, request, redirect, flash, send_file
import os
from services.movie_service import MovieService
from services.director_service import DirectorService
from services.crawler_service import CrawlerService
from services.analysis_service import AnalysisService
from services.io_service import IOService
from models.movie import Movie
from models.director import Director

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "movie_revenue_secret"

movie_service = MovieService()
director_service = DirectorService()
crawler_service = CrawlerService()
analysis_service = AnalysisService()
io_service = IOService()

# Định dạng tiền tệ cho Jinja2
@app.template_filter('format_currency')
def format_currency(value):
    if value is None: return "0"
    return "{:,.0f}".format(value)

@app.route('/')
def index():
    search = request.args.get('search')
    sort = request.args.get('sort')
    director_id = request.args.get('director_id')
    d_id = int(director_id) if director_id and director_id.isdigit() else None
    
    stats = analysis_service.get_statistics(search_query=search, sort_by=sort, director_id=d_id)
    chart = analysis_service.generate_charts()
    return render_template('dashboard.html', stats=stats, chart=chart)

@app.route('/movies')
def list_movies():
    search = request.args.get('search')
    sort = request.args.get('sort')
    director_id = request.args.get('director_id')
    d_id = int(director_id) if director_id and director_id.isdigit() else None
    
    movies = movie_service.get_all_movies(search_query=search, sort_by=sort, director_id=d_id)
    directors = director_service.get_all_directors()
    return render_template('movies.html', movies=movies, directors=directors)

@app.route('/movies/add', methods=['POST'])
def add_movie():
    try:
        title = request.form['title']
        year = int(request.form['year'])
        revenue = float(request.form['revenue'])
        director_id = int(request.form['director_id'])
        movie_service.add_movie(Movie(title=title, year=year, revenue=revenue, director_id=director_id))
        flash("Thêm phim thành công!", "success")
    except Exception as e:
        flash(f"Lỗi: {e}", "error")
    return redirect('/movies')

@app.route('/movies/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    if request.method == 'POST':
        try:
            title = request.form['title']
            year = int(request.form['year'])
            revenue = float(request.form['revenue'])
            director_id = int(request.form['director_id'])
            movie_service.update_movie(Movie(id=movie_id, title=title, year=year, revenue=revenue, director_id=director_id))
            flash("Cập nhật phim thành công!", "success")
            return redirect('/movies')
        except Exception as e:
            flash(f"Lỗi: {e}", "error")
    
    movie = movie_service.get_movie_by_id(movie_id)
    directors = director_service.get_all_directors()
    return render_template('edit_movie.html', movie=movie, directors=directors)

@app.route('/movies/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie_service.delete_movie(movie_id)
    return redirect('/movies')

@app.route('/directors')
def list_directors():
    search = request.args.get('search')
    directors = director_service.get_all_directors(search_query=search)
    return render_template('directors.html', directors=directors)

@app.route('/directors/add', methods=['POST'])
def add_director():
    try:
        name = request.form['name']
        birth_year = int(request.form['birth_year']) if request.form['birth_year'] else None
        director_service.add_director(Director(name=name, birth_year=birth_year))
        flash("Thêm đạo diễn thành công!", "success")
    except Exception as e:
        flash(f"Lỗi: {e}", "error")
    return redirect('/directors')

@app.route('/directors/edit/<int:director_id>', methods=['GET', 'POST'])
def edit_director(director_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            birth_year = int(request.form['birth_year']) if request.form['birth_year'] else None
            director_service.repo.update(Director(id=director_id, name=name, birth_year=birth_year))
            flash("Cập nhật đạo diễn thành công!", "success")
            return redirect('/directors')
        except Exception as e:
            flash(f"Lỗi: {e}", "error")
            
    director = director_service.repo.get_by_id(director_id)
    return render_template('edit_director.html', director=director)

@app.route('/directors/delete/<int:director_id>', methods=['POST'])
def delete_director(director_id):
    try:
        director_service.delete_director(director_id)
        flash("Xóa đạo diễn thành công!", "success")
    except Exception as e:
        flash(f"{e}", "error")
    return redirect('/directors')

@app.route('/crawl', methods=['POST'])
def crawl():
    count = crawler_service.crawl_movies(limit=60)
    if count > 0:
        flash(f"Đã cào thành công {count} phim từ Wikipedia!", "success")
    else:
        flash("Không cào được dữ liệu mới hoặc có lỗi xảy ra.", "error")
    return redirect('/')

@app.route('/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        flash("Không tìm thấy file tải lên.", "error")
        return redirect('/movies')
    
    file = request.files['file']
    if file.filename == '':
        flash("Chưa chọn file.", "error")
        return redirect('/movies')
    
    try:
        if file.filename.endswith('.csv'):
            count = io_service.import_movies_from_csv(file)
            flash(f"Đã nhập thành công {count} phim từ CSV!", "success")
        elif file.filename.endswith('.json'):
            count = io_service.import_movies_from_json(file)
            flash(f"Đã nhập thành công {count} phim từ JSON!", "success")
        else:
            flash("Định dạng file không được hỗ trợ. Vui lòng dùng .csv hoặc .json", "error")
    except Exception as e:
        flash(f"Lỗi nhập liệu: {e}", "error")
        
    return redirect('/movies')

@app.route('/export/csv')
def export_csv():
    file_path = os.path.join(os.path.dirname(__file__), "..", "revenue_report.csv")
    if io_service.export_movies_to_csv(file_path):
        return send_file(file_path, as_attachment=True)
    return "Export failed", 500

@app.route('/export/json')
def export_json():
    file_path = os.path.join(os.path.dirname(__file__), "..", "revenue_report.json")
    if io_service.export_movies_to_json(file_path):
        return send_file(file_path, as_attachment=True)
    return "Export failed", 500
