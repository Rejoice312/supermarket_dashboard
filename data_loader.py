# data_loader.py
import streamlit as st
import pandas as pd

@st.cache_data(show_spinner=False)
def load_data(file_path="data.xlsx"):
    return {
        "sales": pd.read_excel(file_path, sheet_name="sales_transactions"),
        "inventory": pd.read_excel(file_path, sheet_name="inventory_daily_snapshot"),
        "expenses": pd.read_excel(file_path, sheet_name="operating_expenses"),
        "products": pd.read_excel(file_path, sheet_name="products"),
        "suppliers": pd.read_excel(file_path, sheet_name="suppliers")
    }
