import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Profitability & Cost Control | Supermarket Dashboard",
    layout="wide"
)

# -------------------------------------------------
# COLOR SCHEME (CONSISTENT)
# -------------------------------------------------
BACKGROUND_COLOR = "#f5f7fb"
CARD_BACKGROUND = "#ffffff"
PRIMARY_COLOR = "#4f46e5"
SECONDARY_COLOR = "#0f172a"
SUCCESS_COLOR = "#15803d"
WARNING_COLOR = "#d97706"
DANGER_COLOR = "#b91c1c"
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
expenses = data["expenses"]

sales["Transaction Date"] = pd.to_datetime(sales["transaction_date"])
expenses["Expense Date"] = pd.to_datetime(expenses["expense_date"])

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
def total_revenue():
    return sales["total_amount"].sum()

def total_cost_of_goods_sold():
    merged = sales.merge(products, on="product_id")
    return (merged["quantity_sold"] * merged["cost_price"]).sum()

def gross_profit():
    return total_revenue() - total_cost_of_goods_sold()

def gross_margin():
    revenue = total_revenue()
    return round((gross_profit() / revenue) * 100, 2) if revenue else 0

def total_operating_expenses():
    return expenses["expense_amount"].sum()

def net_profit_estimate():
    return gross_profit() - total_operating_expenses()

# -------------------------------------------------
# CHARTS
# -------------------------------------------------
def monthly_profit_trend_chart():
    merged = sales.merge(products, on="product_id")
    merged["Month"] = merged["Transaction Date"].dt.to_period("M").astype(str)

    grouped = merged.groupby("Month").agg(
        Revenue=("total_amount", "sum"),
        Cost=("quantity_sold", lambda x: (x * merged.loc[x.index, "cost_price"]).sum())
    ).reset_index()

    grouped["Gross Profit"] = grouped["Revenue"] - grouped["Cost"]

    fig = px.line(
        grouped,
        x="Month",
        y="Gross Profit",
        markers=True
    )

    fig.update_traces(line=dict(color=SUCCESS_COLOR, width=3))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Month",
        yaxis_title="Gross Profit (₦)",
        yaxis_tickprefix="₦",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

def expense_category_breakdown_chart():
    grouped = expenses.groupby("expense_category")["expense_amount"].sum().reset_index()

    fig = px.bar(
        grouped,
        x="expense_category",
        y="expense_amount"
    )

    fig.update_traces(marker_color=WARNING_COLOR)
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Expense Category",
        yaxis_title="Total Cost (₦)",
        yaxis_tickprefix="₦",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

# -------------------------------------------------
# TABLE
# -------------------------------------------------
def high_cost_products_table():
    merged = sales.merge(products, on="product_id")
    merged["Cost Impact"] = merged["quantity_sold"] * merged["cost_price"]

    table = merged.groupby("product_name").agg(
        Units_Sold=("quantity_sold", "sum"),
        Cost_Impact=("Cost Impact", "sum")
    ).reset_index()

    return table.sort_values("Cost_Impact", ascending=False).head(10).rename(
        columns={
            "product_name": "Product Name",
            "Units_Sold": "Units Sold",
            "Cost_Impact": "Total Cost (₦)"
        }
    )

# -------------------------------------------------
# PAGE LAYOUT
# -------------------------------------------------
st.title("Profitability & Cost Control")

# KPIs
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi_card("Total Revenue", f"₦{total_revenue():,.0f}")

with k2:
    kpi_card("Cost Of Goods Sold", f"₦{total_cost_of_goods_sold():,.0f}")

with k3:
    kpi_card("Gross Profit", f"₦{gross_profit():,.0f}")

with k4:
    kpi_card("Gross Margin", f"{gross_margin()}%")

with k5:
    kpi_card("Net Profit Estimate", f"₦{net_profit_estimate():,.0f}")

# Charts
st.markdown('<div class="section-title">Profitability Trends</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="subheader">Monthly Gross Profit Trend</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="caption">Tracks how gross profit has changed over time.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(monthly_profit_trend_chart(), use_container_width=True)

with right:
    st.markdown('<div class="subheader">Operating Expenses By Category</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="caption">Shows which cost categories consume the most money.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(expense_category_breakdown_chart(), use_container_width=True)

# Table
st.markdown('<div class="section-title">Products With Highest Cost Impact</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="caption">Products that contribute most to total cost of goods sold.</div>',
    unsafe_allow_html=True
)

st.dataframe(high_cost_products_table(), use_container_width=True)
