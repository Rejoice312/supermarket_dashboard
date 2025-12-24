import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Inventory & Stock Health | Supermarket Dashboard",
    layout="wide"
)

# -------------------------------------------------
# COLOR SCHEME (LIGHT & MATURE)
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
inventory = data["inventory"]
products = data["products"]

inventory["Snapshot Date"] = pd.to_datetime(inventory["snapshot_date"])

latest_date = inventory["Snapshot Date"].max()

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
def total_units_in_stock():
    latest = inventory[inventory["Snapshot Date"] == latest_date]
    return int(latest["closing_stock"].sum())

def stockout_rate():
    latest = inventory[inventory["Snapshot Date"] == latest_date]
    return round((latest["closing_stock"] <= 30).mean() * 100, 2)

def damaged_and_expired_units():
    latest = inventory[inventory["Snapshot Date"] == latest_date]
    return int(latest["damaged_qty"].sum() + latest["expired_qty"].sum())

def received_units_today():
    latest = inventory[inventory["Snapshot Date"] == latest_date]
    return int(latest["received_qty"].sum())

def sold_units_today():
    latest = inventory[inventory["Snapshot Date"] == latest_date]
    return int(latest["sold_qty"].sum())

# -------------------------------------------------
# CHARTS
# -------------------------------------------------
def stock_movement_breakdown_chart():
    latest = inventory[inventory["Snapshot Date"] == latest_date]

    summary = pd.DataFrame({
        "Movement Type": [
            "Opening Stock",
            "Received",
            "Sold",
            "Damaged",
            "Expired",
            "Closing Stock"
        ],
        "Units": [
            latest["opening_stock"].sum(),
            latest["received_qty"].sum(),
            latest["sold_qty"].sum(),
            latest["damaged_qty"].sum(),
            latest["expired_qty"].sum(),
            latest["closing_stock"].sum()
        ]
    })

    fig = px.bar(
        summary,
        x="Movement Type",
        y="Units",
        color="Movement Type",
        color_discrete_map={
            "Opening Stock": PRIMARY_COLOR,
            "Received": SUCCESS_COLOR,
            "Sold": INFO_COLOR if "INFO_COLOR" in globals() else PRIMARY_COLOR,
            "Damaged": WARNING_COLOR,
            "Expired": DANGER_COLOR,
            "Closing Stock": SECONDARY_COLOR
        }
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Inventory Movement Type",
        yaxis_title="Units",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

def stock_level_distribution_chart():
    latest = inventory[inventory["Snapshot Date"] == latest_date]

    latest["Stock Status"] = latest["closing_stock"].apply(
        lambda x: "Stockout" if x <= 0 else "In Stock"
    )

    grouped = latest["Stock Status"].value_counts().reset_index()
    grouped.columns = ["Stock Status", "Number Of Products"]

    fig = px.bar(
        grouped,
        x="Stock Status",
        y="Number Of Products",
        color="Stock Status",
        color_discrete_map={
            "In Stock": SUCCESS_COLOR,
            "Stockout": DANGER_COLOR
        }
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=AXIS_COLOR),
        xaxis_title="Stock Status",
        yaxis_title="Number Of Products",
        yaxis_gridcolor=GRID_COLOR
    )

    return fig

# -------------------------------------------------
# TABLES
# -------------------------------------------------
def low_stock_table(threshold=30):
    merged = inventory.merge(products, on="product_id")
    latest = merged[merged["Snapshot Date"] == latest_date]

    table = latest[latest["closing_stock"] <= threshold][[
        "product_name",
        "closing_stock",
        "sold_qty",
        "received_qty"
    ]]

    return table.rename(columns={
        "product_name": "Product Name",
        "closing_stock": "Current Stock",
        "sold_qty": "Units Sold Today",
        "received_qty": "Units Received Today"
    }).sort_values("Current Stock")

# -------------------------------------------------
# PAGE LAYOUT
# -------------------------------------------------
st.title("Inventory & Stock Health")

# KPI ROW
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi_card("Total Units In Stock", f"{total_units_in_stock():,}")

with k2:
    kpi_card("Stockout Rate", f"{stockout_rate()}%")

with k3:
    kpi_card("Damaged & Expired Units", f"{damaged_and_expired_units():,}")

with k4:
    kpi_card("Units Received Today", f"{received_units_today():,}")

with k5:
    kpi_card("Units Sold Today", f"{sold_units_today():,}")

# CHARTS
st.markdown('<div class="section-title">Inventory Movement Overview</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="subheader">Inventory Movement Breakdown</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="caption">Shows how inventory moved today across opening stock, receipts, sales, damage, expiry, and closing stock.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(stock_movement_breakdown_chart(), use_container_width=True)

with right:
    st.markdown('<div class="subheader">Stock Availability Distribution</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="caption">Displays the number of products currently in stock versus those stocked out.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(stock_level_distribution_chart(), use_container_width=True)

# TABLE
st.markdown('<div class="section-title">Low Stock Items (Operational Attention)</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="caption">Products with critically low stock levels based on a fixed operational threshold.</div>',
    unsafe_allow_html=True
)

st.dataframe(low_stock_table(), use_container_width=True)
