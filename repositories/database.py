import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "imdb.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    # Xử lý migration: Nếu bảng cũ có 'rating' thay vì 'revenue', chúng ta sẽ reset DB
    # Đây là cách nhanh nhất cho môi trường phát triển bài tập
    conn = get_connection()
    cursor = conn.cursor()
    
    # Kiểm tra cấu trúc hiện tại
    try:
        cursor.execute("SELECT revenue FROM movies LIMIT 1")
    except sqlite3.OperationalError:
        # Nếu lỗi (nghĩa là chưa có cột revenue), xóa bảng cũ để tạo mới
        print("Cấu trúc DB cũ. Đang dọn dẹp để cập nhật sang Doanh thu...")
        cursor.execute("DROP TABLE IF EXISTS movies")
        cursor.execute("DROP TABLE IF EXISTS directors")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS directors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            revenue REAL,
            director_id INTEGER,
            FOREIGN KEY(director_id) REFERENCES directors(id) ON DELETE RESTRICT
        )
    """)
    
    conn.commit()
    conn.close()
