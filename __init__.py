import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

DB_PATH = Path(__file__).parent / "warehouse.duckdb"

st.set_page_config(page_title="Retail Lakehouse Pipeline", layout="wide")
st.title("Retail Lakehouse Pipeline Dashboard")
st.caption("A data engineering portfolio project built for analytics-ready reporting.")

if not DB_PATH.exists():
    st.error("Database not found. Run `python run_pipeline.py` first.")
    st.stop()

con = duckdb.connect(str(DB_PATH))
kpis = con.execute("""
    SELECT
        COUNT(*) AS total_orders,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(AVG(revenue), 2) AS avg_order_revenue,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM fct_sales
""").df().iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Orders", int(kpis["total_orders"]))
c2.metric("Revenue", f"${kpis['total_revenue']:,.2f}")
c3.metric("Avg order revenue", f"${kpis['avg_order_revenue']:,.2f}")
c4.metric("Customers", int(kpis["unique_customers"]))

trend = con.execute("SELECT order_date, revenue FROM mart_daily_revenue ORDER BY order_date").df()
fig = px.line(trend, x="order_date", y="revenue", title="Daily revenue")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    region = con.execute("""
        SELECT customer_region, ROUND(SUM(revenue), 2) AS revenue
        FROM fct_sales
        GROUP BY customer_region
        ORDER BY revenue DESC
    """).df()
    st.subheader("Revenue by region")
    st.dataframe(region, use_container_width=True)

with right:
    products = con.execute("""
        SELECT product_name, SUM(quantity) AS units_sold, ROUND(SUM(revenue), 2) AS revenue
        FROM fct_sales
        GROUP BY product_name
        ORDER BY revenue DESC
        LIMIT 10
    """).df()
    st.subheader("Top products")
    st.dataframe(products, use_container_width=True)

st.subheader("Fact sales sample")
st.dataframe(con.execute("SELECT * FROM fct_sales LIMIT 20").df(), use_container_width=True)
