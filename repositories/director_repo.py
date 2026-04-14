from models.director import Director
from repositories.database import get_connection

class DirectorRepository:
    def get_all(self, search_query=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "SELECT * FROM directors"
        params = []
        
        if search_query:
            sql += " WHERE name LIKE ?"
            params.append(f"%{search_query}%")
            
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [Director(id=r["id"], name=r["name"], birth_year=r["birth_year"]) for r in rows]

    def get_by_id(self, director_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM directors WHERE id = ?", (director_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Director(id=row["id"], name=row["name"], birth_year=row["birth_year"])
        return None

    def add(self, director: Director):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO directors (name, birth_year) VALUES (?, ?)", 
                       (director.name, director.birth_year))
        conn.commit()
        director.id = cursor.lastrowid
        conn.close()
        return director

    def update(self, director: Director):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE directors SET name = ?, birth_year = ? WHERE id = ?", 
                       (director.name, director.birth_year, director.id))
        conn.commit()
        conn.close()

    def delete(self, director_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM directors WHERE id = ?", (director_id,))
        conn.commit()
        conn.close()
