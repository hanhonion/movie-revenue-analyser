# Movie Revenue Analyser - Dự án Wikipedia Movie Crawler

Dự án này là một ứng dụng web xây dựng bằng Python/Flask, cho phép cào dữ liệu phim từ Wikipedia, quản lý cơ sở dữ liệu phim/đạo diễn và phân tích doanh thu bằng biểu đồ thông minh.

## 🌟 Tính năng nổi bật

### 1. Thu thập dữ liệu (Crawler)
*   **Deep Crawling**: Hệ thống không chỉ cào danh sách phim mà còn tự động truy cập vào trang cá nhân của từng Đạo diễn trên Wikipedia để mang về tên và **năm sinh** chuẩn xác.
*   **Kho dữ liệu lớn**: Hỗ trợ cào hơn **50 bộ phim** doanh thu cao nhất mọi thời đại chỉ với một nút bấm.

### 2. Quản lý dữ liệu (CRUD)
*   **Movie Management**: Thêm, sửa, xóa và tìm kiếm phim theo tiêu đề.
*   **Director Management**: Quản lý danh sách đạo diễn, hỗ trợ tìm kiếm theo tên.
*   **Sắp xếp & Lọc**: Sắp xếp phim theo doanh thu (cao/thấp), theo năm, hoặc lọc phim theo từng đạo diễn cụ thể.

### 3. Quy tắc nghiệp vụ (Business Rules)
Hệ thống triển khai 5 luật kiểm soát dữ liệu nghiêm ngặt:
1. Doanh thu phim không được phép là số âm.
2. Năm phát hành phim phải hợp lệ (từ 1888 đến tương lai 5 năm).
3. Chống trùng lặp phim (không cho phép trùng cả Tên và Năm).
4. Ràng buộc toàn vẹn: Không cho phép xóa Đạo diễn nếu họ vẫn còn phim trong hệ thống.
5. Kiểm tra thông tin Đạo diễn (Tên không trống, năm sinh không ở tương lai).

### 4. Báo cáo & Thống kê (Analysis)
*   **Dashboard**: Hiển thị Tổng doanh thu, Trung bình và Top 5 phim.
*   **Biểu đồ Matplotlib**: Tích hợp 2 biểu đồ trực quan (Xu hướng doanh thu theo năm và Top 5 phim cao nhất).

### 5. Nhập/Xuất dữ liệu (I/O)
*   **Export**: Xuất báo cáo toàn bộ danh sách phim ra định dạng **CSV** và **JSON** (Nút màu tím và xanh tại Dashboard).
*   **Import (Nạp dữ liệu)**: Khả năng nạp dữ liệu từ file **CSV** hoặc **JSON**.
    *   Vị trí: Ngay tại **Dashboard** hoặc trang **Movies**.
    *   Hệ thống có kiểm tra định dạng file và xử lý dữ liệu lỗi trước khi nạp vào DB.

---

## 🛠 Công nghệ sử dụng
*   **Ngôn ngữ**: Python 3.x
*   **Web Framework**: Flask
*   **Cơ sở dữ liệu**: SQLite3 (với mô hình Repository & OOP)
*   **Thư viện đồ họa**: Matplotlib (Backend Agg)
*   **Scraping**: BeautifulSoup4 & Requests

---

## 🚀 Hướng dẫn khởi chạy

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt Python. Sau đó chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
Di chuyển vào thư mục dự án và chạy file `main.py`:
```bash
python main.py
```

### 3. Truy cập
Mở trình duyệt và truy cập địa chỉ: `http://127.0.0.1:5000`

---

## 📁 Cấu trúc thư mục
* `/models`: Định nghĩa lớp Movie, Director.
* `/repositories`: Lớp tương tác trực tiếp với Database SQLite.
* `/services`: Lớp xử lý logic nghiệp vụ, crawler, phân tích và I/O.
* `/ui`: Chứa logic Flask (app.py) và các giao diện HTML (templates).
* `main.py`: File khởi chạy toàn bộ hệ thống.
