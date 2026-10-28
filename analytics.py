"""Các hàm phân tích dữ liệu bán hàng sử dụng Polars."""
from pathlib import Path
import polars as pl

REQUIRED_COLUMNS = {"order_id", "date", "product", "category", "quantity", "unit_price"}


def load_sales(path: str | Path = "data/sales.csv", *, lazy: bool = False):
    """Đọc CSV, kiểm tra cột, chuyển kiểu và loại bỏ các dòng không hợp lệ."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {path}")

    if lazy:
        frame = pl.scan_csv(path, try_parse_dates=False)
        columns = set(frame.collect_schema().names())
    else:
        frame = pl.read_csv(path, try_parse_dates=False)
        columns = set(frame.columns)

    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise ValueError("Thiếu cột bắt buộc: " + ", ".join(sorted(missing)))

    frame = frame.with_columns(
        pl.col("order_id").cast(pl.Int64, strict=False),
        pl.col("date").str.to_date(strict=False),
        pl.col("product").cast(pl.String).str.strip_chars(),
        pl.col("category").cast(pl.String).str.strip_chars(),
        pl.col("quantity").cast(pl.Int64, strict=False),
        pl.col("unit_price").cast(pl.Float64, strict=False),
    ).with_columns(
        (pl.col("quantity") * pl.col("unit_price")).alias("revenue")
    ).filter(
        pl.col("order_id").is_not_null()
        & pl.col("date").is_not_null()
        & pl.col("product").is_not_null()
        & (pl.col("product") != "")
        & pl.col("quantity").is_not_null()
        & (pl.col("quantity") > 0)
        & pl.col("unit_price").is_not_null()
        & (pl.col("unit_price") >= 0)
    )
    return frame


def summary(data: pl.DataFrame) -> dict:
    """Tạo các chỉ số tổng quan từ DataFrame đã được làm sạch."""
    row = data.select(
        pl.len().alias("valid_rows"),
        pl.col("order_id").n_unique().alias("orders"),
        pl.col("quantity").sum().alias("units_sold"),
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("revenue").mean().alias("average_line_revenue"),
    ).row(0, named=True)
    return {key: (0 if value is None else value) for key, value in row.items()}


def top_products(data: pl.DataFrame, limit: int = 5) -> pl.DataFrame:
    if limit < 1:
        raise ValueError("limit phải lớn hơn hoặc bằng 1")
    return (
        data.group_by("product")
        .agg(
            pl.col("quantity").sum().alias("units_sold"),
            pl.col("revenue").sum().round(2).alias("total_revenue"),
        )
        .sort("total_revenue", descending=True)
        .head(limit)
    )


def monthly_revenue(data: pl.DataFrame) -> pl.DataFrame:
    return (
        data.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("month"))
        .group_by("month")
        .agg(
            pl.col("order_id").n_unique().alias("orders"),
            pl.col("quantity").sum().alias("units_sold"),
            pl.col("revenue").sum().round(2).alias("total_revenue"),
        )
        .sort("month")
    )
