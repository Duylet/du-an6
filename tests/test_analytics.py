from pathlib import Path
import polars as pl
import pytest
from analytics import load_sales, monthly_revenue, summary, top_products

DATA = Path(__file__).resolve().parents[1] / "data" / "sales.csv"


def test_load_sales_has_revenue_column():
    data = load_sales(DATA)
    assert data.height == 12
    assert "revenue" in data.columns
    assert data["revenue"].sum() > 0


def test_summary_counts_rows_and_orders():
    metrics = summary(load_sales(DATA))
    assert metrics["valid_rows"] == 12
    assert metrics["orders"] == 12
    assert metrics["units_sold"] == 25


def test_top_products_is_sorted_by_revenue():
    result = top_products(load_sales(DATA), limit=3)
    assert result.height == 3
    revenues = result["total_revenue"].to_list()
    assert revenues == sorted(revenues, reverse=True)


def test_top_products_rejects_invalid_limit():
    with pytest.raises(ValueError):
        top_products(load_sales(DATA), limit=0)


def test_monthly_revenue_has_month_column():
    result = monthly_revenue(load_sales(DATA))
    assert result.columns == ["month", "orders", "units_sold", "total_revenue"]
    assert result.height == 4


def test_lazy_loading_matches_eager():
    eager = load_sales(DATA)
    lazy = load_sales(DATA, lazy=True).collect()
    assert eager.equals(lazy)
