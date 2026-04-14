import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from repositories.database import init_db
from ui.app import app

if __name__ == "__main__":
    print("--- KHỞI KHỞI CHẠY DỰ ÁN IMDb ANALYSER ---")
    
    # 1. Khởi tạo Database (Tạo bảng nếu chưa có)
    print("Đang khởi tạo cơ sở dữ liệu...")
    init_db()
    
    # 2. Khởi chạy Flask Server
    # Chạy trên port 5000 mặc định
    print("Máy chủ đang chạy tại: http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
