from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    year: int
    revenue: float # Đổi từ rating sang revenue (Doanh thu $)
    director_id: int
    id: int = None
