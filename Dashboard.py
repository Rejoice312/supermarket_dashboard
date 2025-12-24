import streamlit as st

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Nigerian Supermarket BI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# COLOR SCHEME (LIGHT & MATURE)
# -------------------------------------------------
BACKGROUND_COLOR = "#f5f7fb"          # Soft light background
SIDEBAR_BACKGROUND = "#ffffff"        # Clean white
PRIMARY_COLOR = "#4f46e5"              # Muted indigo
SECONDARY_COLOR = "#0f172a"            # Deep slate text
MUTED_TEXT = "#64748b"                 # Subtle gray
DIVIDER_COLOR = "#e5e7eb"              # Light divider
INFO_BACKGROUND = "#eef2ff"            # Soft indigo tint
INFO_BORDER = "#c7d2fe"

# -------------------------------------------------
# GLOBAL INLINE CSS
# -------------------------------------------------
st.markdown(
    f"""
    <style>

    /* App background */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}

    /* Sidebar background */
    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BACKGROUND};
        border-right: 1px solid {DIVIDER_COLOR};
    }}

    /* Sidebar padding */
    section[data-testid="stSidebar"] > div {{
        padding-top: 20px;
    }}

    /* Headings */
    h1, h2, h3 {{
        color: {SECONDARY_COLOR};
    }}

    /* Paragraph text */
    p, li {{
        color: {SECONDARY_COLOR};
        font-size: 15px;
        line-height: 1.6;
    }}

    /* Muted text */
    .muted {{
        color: {MUTED_TEXT};
        font-size: 14px;
    }}

    /* Sidebar title */
    .sidebar-title {{
        font-size: 22px;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin-bottom: 2px;
    }}

    /* Sidebar subtitle */
    .sidebar-subtitle {{
        font-size: 13px;
        color: {MUTED_TEXT};
        margin-bottom: 16px;
    }}

    /* Sidebar section header */
    .sidebar-section {{
        font-size: 14px;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin: 18px 0 6px 0;
    }}

    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background-color: {DIVIDER_COLOR};
        margin: 16px 0;
    }}

    /* Info box override */
    div[data-testid="stAlert"] {{
        background-color: {INFO_BACKGROUND};
        border: 1px solid {INFO_BORDER};
        color: {SECONDARY_COLOR};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# SIDEBAR CONTENT
# -------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div>
            <div class="sidebar-title">Supermarket BI</div>
            <div class="sidebar-subtitle">
                Operations & Performance Dashboard
            </div>
        </div>
        <hr>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-section">What this dashboard helps you do</div>
        <ul class="muted">
            <li>Monitor daily business performance</li>
            <li>Detect inventory risks early</li>
            <li>Control operating and energy costs</li>
            <li>Make data-driven decisions confidently</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        """
        <p class="muted">
            Data Period: January – December (1 Year)<br>
            Location: Lagos, Nigeria
        </p>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# MAIN LANDING CONTENT
# -------------------------------------------------
st.markdown(
    """
    <h1>Supermarket Operations Dashboard</h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p>
    Welcome to the <strong>Supermarket Business Intelligence Dashboard</strong>.
    </p>

    <p>
    This application is built to support <strong>supermarket managers and owners</strong>
    with clear visibility into operations, inventory health, costs, and sales performance.
    </p>

    <h3>How to use this dashboard</h3>
    <ul>
        <li>Use the <strong>sidebar navigation</strong> to switch between pages</li>
        <li>Each page focuses on a <strong>specific managerial concern</strong></li>
        <li>KPIs and visuals are generated from real operational data</li>
    </ul>

    <h3>Core focus areas</h3>
    <ul>
        <li>Executive performance overview</li>
        <li>Inventory and stock health</li>
        <li>Profitability and cost control</li>
        <li>Sales trends and demand behavior</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.info(
    "Start with **Executive Overview** to get a one-glance view of today’s business health."
)
