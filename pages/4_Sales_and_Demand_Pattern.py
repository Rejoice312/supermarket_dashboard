import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Sales & Demand Patterns | Supermarket Dashboard",
    layout="wide"
)

# -------------------------------------------------
# COLOR SCHEME (SAME AS OTHER PAGES)
# -------------------------------------------------
BACKGROUND_COLOR = "#f5f7fb"
CARD_BACKGROUND = "#ffffff"
PRIMARY_COLOR = "#4f46e5"
SECONDARY_COLOR = "#0f172a"
SUCCESS_COLOR = "#15803d"
WARNING_COLOR = "#d97706"
INFO_COLOR = "#0369a1"
AXIS_COLOR = "#334155"
GRID_COLOR = "#e2e8f0"
MUTED_TEXT = "#64748b"

# -------------------------------------------------
# INLINE CSS
# -------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}

    .kpi-card {{
        background-color: {CARD_BACKGROUND};
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.05);
        text-align: center;
    }}

    .kpi-title {{
        font-size: 12px;
        color: {MUTED_TEXT};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}

    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        color: {SECONDARY_COLOR};
    }}

    .section-title {{
        font-size: 24px;
        font-weight: 700;
        margin: 32px 0 10px 0;
        color: {SECONDARY_COLOR};
    }}

    .subheader {{
        font-size: 18px;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin-bottom: 4px;
    }}

    .caption {{
        font-size: 13px;
        color: {MUTED_TEXT};
        margin-bottom: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

data = load_data()
sales = data["sales"]
products = data["products"]

sales["Transaction Date"] = pd.to_datetime(sales["transaction_date"])
sales["Hour"] = sales["Transaction Date"].dt.hour
sales["Day Of Week"] = sales["Transaction Date"].dt.day_name()
sales["Month"] = sales["Transaction Date"].dt.to_period("M").astype(str)

# -------------------------------------------------
# KPI COMPONENT
# -------------------------------------------------
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

# -------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------
def total_units_sold():
    return sales["quantity_sold"].sum()

def average_daily_sales():
    daily = sales.groupby(sales["Transaction Date"].dt.date)["total_amount"].sum()
    return daily.mean()

def peak_sales_hour():
    return sales.groupby("Hour")["total_amount"].sum().idxmax()

def best_selling_category():
    merged = sales.merge(products, on="product_id")
    return (
        merged.groupby("category")["quantity_sold"]
        .sum()
        .idxmax()
    )

# -------------------------------------------------
# CHARTS
# -------------------------------------------------
def hourly_sales_pattern_chart():
    grouped = sales.groupby("Hour")["total_amount"].sum().reset_index()

    fig = px.line(
        grouped,
        x="Hour",
        y="total_amount",
        markers=True
    )

    fig.update_traces(line=dict(color=PRIMARY_COLOR, width=3))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Hour Of Day",
        yaxis_title="Total Sales (₦)",
        yaxis_tickprefix="₦",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

def day_of_week_sales_chart():
    order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    grouped = (
        sales.groupby("Day Of Week")["total_amount"]
        .sum()
        .reindex(order)
        .reset_index()
    )

    fig = px.bar(
        grouped,
        x="Day Of Week",
        y="total_amount"
    )

    fig.update_traces(marker_color=INFO_COLOR)
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Day Of Week",
        yaxis_title="Total Sales (₦)",
        yaxis_tickprefix="₦",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

def monthly_category_demand_chart():
    merged = sales.merge(products, on="product_id")

    grouped = merged.groupby(
        ["Month", "category"]
    )["quantity_sold"].sum().reset_index()

    fig = px.area(
        grouped,
        x="Month",
        y="quantity_sold",
        color="category"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Month",
        yaxis_title="Units Sold",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

# -------------------------------------------------
# TABLE
# -------------------------------------------------
def top_products_by_volume_table():
    merged = sales.merge(products, on="product_id")

    table = merged.groupby("product_name").agg(
        Units_Sold=("quantity_sold", "sum"),
        Revenue=("total_amount", "sum")
    ).reset_index()

    return table.sort_values(
        "Units_Sold", ascending=False
    ).head(10).rename(
        columns={
            "product_name": "Product Name",
            "Units_Sold": "Units Sold",
            "Revenue": "Total Revenue (₦)"
        }
    )

# -------------------------------------------------
# PAGE LAYOUT
# -------------------------------------------------
st.title("Sales & Demand Patterns")

# KPIs
k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Total Units Sold", f"{total_units_sold():,}")

with k2:
    kpi_card("Average Daily Sales", f"₦{average_daily_sales():,.0f}")

with k3:
    kpi_card("Peak Sales Hour", f"{peak_sales_hour()}:00")

with k4:
    kpi_card("Top Selling Category", best_selling_category())

# Charts
st.markdown('<div class="section-title">Customer Buying Behavior</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="subheader">Hourly Sales Pattern</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="caption">Identifies peak shopping hours for staff and power planning.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(hourly_sales_pattern_chart(), use_container_width=True)

with right:
    st.markdown('<div class="subheader">Sales By Day Of Week</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="caption">Shows which days drive the highest demand.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(day_of_week_sales_chart(), use_container_width=True)

st.markdown('<div class="section-title">Demand Trends</div>', unsafe_allow_html=True)

st.markdown('<div class="subheader">Monthly Category Demand</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="caption">Tracks how product categories perform across the year.</div>',
    unsafe_allow_html=True
)
st.plotly_chart(monthly_category_demand_chart(), use_container_width=True)

# Table
st.markdown('<div class="section-title">Top Selling Products</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="caption">Products with the highest sales volume.</div>',
    unsafe_allow_html=True
)

st.dataframe(top_products_by_volume_table(), use_container_width=True)
