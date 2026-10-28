"""CLI demo phân tích bán hàng với Polars."""
import argparse
from pathlib import Path
import polars as pl
from analytics import load_sales, monthly_revenue, summary, top_products


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo phân tích CSV bằng Polars")
    parser.add_argument("--input", default="data/sales.csv", help="Đường dẫn file CSV đầu vào")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in [
        ("summary", "Hiển thị số liệu tổng quan"),
        ("top-products", "Xếp hạng sản phẩm theo doanh thu"),
        ("monthly", "Tổng hợp doanh thu theo tháng"),
    ]:
        command = sub.add_parser(name, help=help_text)
        command.add_argument("--lazy", action="store_true", help="Đọc bằng lazy query")
        command.add_argument("--output", help="Xuất bảng kết quả ra CSV")
        if name == "top-products":
            command.add_argument("--limit", type=int, default=5, help="Số sản phẩm cần hiển thị")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        loaded = load_sales(args.input, lazy=args.lazy)
        data = loaded.collect() if args.lazy else loaded
        print(f"Đã đọc và làm sạch dữ liệu: {data.height} dòng hợp lệ")

        if args.command == "summary":
            metrics = summary(data)
            print("\n=== TỔNG QUAN BÁN HÀNG ===")
            labels = {
                "valid_rows": "Số dòng hợp lệ",
                "orders": "Số đơn hàng khác nhau",
                "units_sold": "Tổng sản phẩm đã bán",
                "total_revenue": "Tổng doanh thu (VND)",
                "average_line_revenue": "Doanh thu trung bình mỗi dòng (VND)",
            }
            for key, label in labels.items():
                print(f"{label}: {metrics[key]:,.2f}" if isinstance(metrics[key], float) else f"{label}: {metrics[key]:,}")
            return 0

        result = top_products(data, args.limit) if args.command == "top-products" else monthly_revenue(data)
        print(result)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            result.write_csv(output)
            print(f"\nĐã lưu báo cáo: {output}")
        return 0
    except (FileNotFoundError, ValueError, pl.exceptions.PolarsError) as exc:
        print(f"Lỗi: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
