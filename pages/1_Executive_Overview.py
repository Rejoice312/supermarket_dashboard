import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from data_loader import load_data

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Executive Overview | Supermarket Dashboard",
    layout="wide"
)

# ----------------------------------
# LIGHT MATURE COLOR SCHEME
# ----------------------------------
BACKGROUND_COLOR = "#f5f7fb"     # Soft light background
CARD_BACKGROUND = "#ffffff"

PRIMARY_COLOR = "#4f46e5"        # Muted Indigo Blue
ACCENT_COLOR = "#10b981"         # Emerald Green
WARNING_COLOR = "#f59e0b"
DANGER_COLOR = "#dc2626"

TEXT_PRIMARY = "#0f172a"         # Deep Slate
TEXT_MUTED = "#64748b"

AXIS_COLOR = "#334155"
GRID_COLOR = "#e5e7eb"

# ----------------------------------
# LOAD DATA
# ----------------------------------

data = load_data()

sales = data["sales"]
inventory = data["inventory"]
expenses = data["expenses"]
products = data["products"]

sales["Transaction Date"] = pd.to_datetime(sales["transaction_date"])
inventory["Snapshot Date"] = pd.to_datetime(inventory["snapshot_date"])
expenses["Expense Date"] = pd.to_datetime(expenses["expense_date"])

today = sales["Transaction Date"].max()
last_30_days = today - timedelta(days=30)

# ----------------------------------
# GLOBAL CSS (STREAMLIT UI THEMING)
# ----------------------------------
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_PRIMARY};
        font-family: Inter, sans-serif;
    }}

    .kpi-card {{
        background-color: {CARD_BACKGROUND};
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
    }}

    .kpi-title {{
        font-size: 12px;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }}

    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        color: {TEXT_PRIMARY};
    }}

    .section-title {{
        font-size: 26px;
        font-weight: 700;
        margin: 36px 0 10px 0;
        color: {TEXT_PRIMARY};
    }}

    .subheader {{
        font-size: 18px;
        font-weight: 600;
        margin-top: 6px;
        color: {TEXT_PRIMARY};
    }}

    .caption {{
        font-size: 13px;
        color: {TEXT_MUTED};
        margin-bottom: 12px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# KPI COMPONENT
# ----------------------------------
def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------
# KPI CALCULATIONS
# ----------------------------------
def calculate_today_revenue():
    return sales[sales["Transaction Date"] == today]["total_amount"].sum()

def calculate_gross_margin():
    merged = sales.merge(products, on="product_id")
    revenue = merged["total_amount"].sum()
    cost = (merged["quantity_sold"] * merged["cost_price"]).sum()
    return round((revenue - cost) / revenue * 100, 2)

def calculate_stockout_rate():
    stockouts = inventory[inventory["closing_stock"] <= 0]
    return round(len(stockouts) / len(inventory) * 100, 2)

def calculate_expired_stock_value():
    merged = inventory.merge(products, on="product_id")
    return (merged["expired_qty"] * merged["cost_price"]).sum()

def calculate_energy_cost_today():
    energy = expenses[
        (expenses["Expense Date"] == today) &
        (expenses["expense_category"] == "Power & Generator Fuel")
    ]
    return energy["expense_amount"].sum()

# ----------------------------------
# CHARTS
# ----------------------------------
def revenue_trend_chart():
    df = sales[sales["Transaction Date"] >= last_30_days]
    grouped = df.groupby("Transaction Date")["total_amount"].sum().reset_index()

    fig = px.line(
        grouped,
        x="Transaction Date",
        y="total_amount",
        markers=True
    )

    fig.update_traces(
        line=dict(color=PRIMARY_COLOR, width=3),
        marker=dict(size=6, color=PRIMARY_COLOR),
        hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Revenue:</b> ₦%{y:,.0f}<extra></extra>"
    )

    fig.update_layout(
        plot_bgcolor=CARD_BACKGROUND,
        paper_bgcolor=CARD_BACKGROUND,
        font=dict(color=AXIS_COLOR),
        xaxis=dict(title="Date", gridcolor=GRID_COLOR),
        yaxis=dict(title="Revenue (₦)", tickprefix="₦", gridcolor=GRID_COLOR),
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return fig

def top_categories_chart():
    grouped = sales.groupby("product_category")["total_amount"].sum().reset_index()
    grouped = grouped.sort_values("total_amount", ascending=False).head(5)

    fig = px.bar(
        grouped,
        x="product_category",
        y="total_amount"
    )

    fig.update_traces(
        marker_color=ACCENT_COLOR,
        hovertemplate="<b>Category:</b> %{x}<br><b>Revenue:</b> ₦%{y:,.0f}<extra></extra>"
    )

    fig.update_layout(
        plot_bgcolor=CARD_BACKGROUND,
        paper_bgcolor=CARD_BACKGROUND,
        font=dict(color=AXIS_COLOR),
        xaxis_title="Product Category",
        yaxis_title="Revenue (₦)",
        yaxis_tickprefix="₦",
        xaxis_gridcolor=GRID_COLOR,
        yaxis_gridcolor=GRID_COLOR,
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return fig

# ----------------------------------
# ALERT TABLE
# ----------------------------------
def low_stock_alert_table():
    alerts = inventory[inventory["closing_stock"] <= 30]
    alerts = alerts.merge(products, on="product_id")

    return alerts[[
        "product_name",
        "closing_stock",
        "reorder_level"
    ]].rename(columns={
        "product_name": "Product Name",
        "closing_stock": "Current Stock",
        "reorder_level": "Reorder Level"
    }).sort_values("Current Stock")

# ----------------------------------
# PAGE LAYOUT
# ----------------------------------
st.title("Executive Overview")

# KPI ROW
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi_card("Today’s Revenue", f"₦{calculate_today_revenue():,.0f}")
with k2:
    kpi_card("Gross Margin", f"{calculate_gross_margin()}%")
with k3:
    kpi_card("Stockout Rate", f"{calculate_stockout_rate()}%")
with k4:
    kpi_card("Expired Stock Value", f"₦{calculate_expired_stock_value():,.0f}")
with k5:
    kpi_card("Energy Cost Today", f"₦{calculate_energy_cost_today():,.0f}")

# SALES PERFORMANCE
st.markdown('<div class="section-title">Sales Performance</div>', unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="subheader">Daily Revenue Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="caption">Daily total revenue over the last 30 days.</div>', unsafe_allow_html=True)
    st.plotly_chart(revenue_trend_chart(), use_container_width=True)

with right:
    st.markdown('<div class="subheader">Top Revenue Categories</div>', unsafe_allow_html=True)
    st.markdown('<div class="caption">Product categories generating the most revenue.</div>', unsafe_allow_html=True)
    st.plotly_chart(top_categories_chart(), use_container_width=True)

# ALERTS
st.markdown('<div class="section-title">Operational Alerts</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Low Stock Items</div>', unsafe_allow_html=True)
st.markdown('<div class="caption">Products approaching critical stock levels.</div>', unsafe_allow_html=True)

st.dataframe(low_stock_alert_table(), use_container_width=True)
