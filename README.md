# Polars Analytics Demo

Dự án demo sử dụng **[Polars](https://github.com/pola-rs/polars)** để đọc, làm sạch và phân tích dữ liệu bán hàng bằng Python. Phù hợp để chạy và học trên VS Code.

## Tính năng

- Đọc dữ liệu CSV bằng Polars.
- Kiểm tra và chuẩn hóa kiểu dữ liệu, bỏ dòng thiếu thông tin quan trọng.
- Thống kê doanh thu, số đơn hàng và giá trị đơn trung bình.
- Xếp hạng sản phẩm theo doanh thu.
- Tổng hợp doanh thu theo tháng.
- Hỗ trợ chế độ eager và lazy query.
- Xuất báo cáo CSV và có unit test bằng pytest.

## 1. Yêu cầu

- Python 3.10 trở lên
- VS Code (khuyến nghị)

## 2. Cài đặt trong VS Code

Mở thư mục dự án trong VS Code, mở Terminal và chạy:

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Nếu PowerShell chặn kích hoạt môi trường, có thể chạy trực tiếp bằng `.venv\Scripts\python.exe` hoặc mở terminal Command Prompt.

## 3. Chạy chương trình

Dữ liệu mẫu nằm trong `data/sales.csv`.

```powershell
python main.py summary
python main.py top-products --limit 5
python main.py monthly
python main.py top-products --limit 3 --output reports/top_products.csv
python main.py monthly --output reports/monthly.csv
```

Thêm `--lazy` để chạy truy vấn theo API lazy của Polars:

```powershell
python main.py summary --lazy
python main.py top-products --limit 5 --lazy
```

Nếu không truyền đường dẫn dữ liệu, chương trình mặc định dùng `data/sales.csv`. Có thể chỉ định file khác bằng `--input`.

```powershell
python main.py summary --input data/sales.csv
```

## 4. Ví dụ kết quả

Lệnh `summary` hiển thị số dòng hợp lệ, tổng doanh thu, số lượng sản phẩm bán ra và giá trị trung bình mỗi đơn. `top-products` xếp sản phẩm theo doanh thu giảm dần; `monthly` nhóm dữ liệu theo tháng.

## 5. Cấu trúc thư mục

```text
du-an6/
├── data/
│   └── sales.csv
├── reports/              # Tạo khi xuất báo cáo
├── tests/
│   └── test_analytics.py
├── analytics.py
├── main.py
├── requirements.txt
└── README.md
```

## 6. Chạy kiểm thử

```powershell
python -m pytest -v
```

## 7. Kiến thức Polars được sử dụng

- `pl.read_csv()`: đọc CSV.
- `with_columns()`: tạo hoặc chuyển đổi cột.
- `filter()`: lọc dòng dữ liệu.
- `group_by().agg()`: tổng hợp theo nhóm.
- `sort()`: sắp xếp kết quả.
- `pl.scan_csv()`: tạo lazy query; truy vấn thực thi khi gọi `collect()`.

**Lưu ý:** Đây là dự án học tập minh họa cách dùng Polars, không phải bản sao của toàn bộ mã nguồn Polars.
