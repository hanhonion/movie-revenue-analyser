from models.movie import Movie
from repositories.database import get_connection

class MovieRepository:
    def get_all(self, search_query=None, sort_by=None, director_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "SELECT * FROM movies WHERE 1=1"
        params = []
        
        if search_query:
            sql += " AND title LIKE ?"
            params.append(f"%{search_query}%")
            
        if director_id:
            sql += " AND director_id = ?"
            params.append(director_id)
            
        if sort_by == 'revenue_desc':
            sql += " ORDER BY revenue DESC"
        elif sort_by == 'year_desc':
            sql += " ORDER BY year DESC"
        elif sort_by == 'title_asc':
            sql += " ORDER BY title ASC"
            
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [Movie(id=r["id"], title=r["title"], year=r["year"], revenue=r["revenue"], director_id=r["director_id"]) for r in rows]

    def get_by_id(self, movie_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Movie(id=row["id"], title=row["title"], year=row["year"], revenue=row["revenue"], director_id=row["director_id"])
        return None

    def add(self, movie: Movie):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movies (title, year, revenue, director_id) VALUES (?, ?, ?, ?)", 
                       (movie.title, movie.year, movie.revenue, movie.director_id))
        conn.commit()
        movie.id = cursor.lastrowid
        conn.close()
        return movie

    def update(self, movie: Movie):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE movies SET title = ?, year = ?, revenue = ?, director_id = ? WHERE id = ?", 
                       (movie.title, movie.year, movie.revenue, movie.director_id, movie.id))
        conn.commit()
        conn.close()

    def delete(self, movie_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()
        conn.close()
        
    def find_by_title_and_year(self, title: str, year: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE title = ? AND year = ?", (title, year))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Movie(id=row["id"], title=row["title"], year=row["year"], revenue=row["revenue"], director_id=row["director_id"])
        return None
