"""TikTok Seller Suite — Main Dashboard."""

import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_dashboard_stats, get_products, get_sales, get_orders

# Auto-seed on first run (e.g., Streamlit Cloud deployment)
if not get_products():
    import seed_data  # noqa: F401

st.set_page_config(
    page_title="TikTok Seller Suite",
    page_icon="💰",
    layout="wide",
)

# Mobile-friendly responsive CSS
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stMainBlockContainer { padding-left: 1rem !important; padding-right: 1rem !important; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
        [data-testid="stMetric"] { padding: 0.5rem !important; }
        .stTabs [data-baseweb="tab-list"] { flex-wrap: wrap !important; gap: 0.25rem !important; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.1rem !important; }
        .stButton > button { min-height: 48px !important; font-size: 1rem !important; }
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div { min-height: 44px !important; font-size: 1rem !important; }
        .stTextArea > div > div > textarea { font-size: 1rem !important; }
        [data-testid="stTable"], .stDataFrame { overflow-x: auto !important; }
        [data-testid="stSidebar"] { min-width: 250px !important; max-width: 250px !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("TikTok Seller Suite")
st.markdown("Your all-in-one dashboard for sourcing, pricing, and selling products on TikTok Shop.")

# --- Key Metrics ---
stats = get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", stats["total_products"])
col2.metric("Active Products", stats["active_products"])
col3.metric("Total Revenue", f"${stats['total_revenue']:,.2f}")
col4.metric("Total Sales", f"{stats['total_sales']:,}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Inventory Units", f"{stats['total_inventory']:,}")
col2.metric("Suppliers", stats["total_suppliers"])
col3.metric("Pending Orders", stats["pending_orders"])
col4.metric("Total Costs", f"${stats['total_cost']:,.2f}")

st.divider()

# --- Charts ---
left, right = st.columns(2)

with left:
    st.subheader("Products by Niche")
    products = get_products()
    if products:
        df = pd.DataFrame(products)
        niche_counts = df["niche"].value_counts().reset_index()
        niche_counts.columns = ["niche", "count"]
        fig = px.pie(niche_counts, values="count", names="niche",
                     color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add products in the **Product Manager** to see charts.")

with right:
    st.subheader("Profit Margins")
    if products:
        df = pd.DataFrame(products)
        df["profit"] = df["selling_price"] - df["source_cost"]
        fig = px.bar(df, x="name", y=["source_cost", "profit"],
                     title="Cost vs Profit per Product",
                     color_discrete_sequence=["#ff0050", "#00f2ea"],
                     barmode="stack")
        fig.update_layout(xaxis_title="", yaxis_title="$", legend_title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No product data yet.")

st.divider()

# --- Recent Orders ---
st.subheader("Recent Orders")
orders = get_orders()
if orders:
    for order in orders[:5]:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{order['product_name'] or 'Unknown'}** x{order['quantity']}")
        col2.write(f"${order['total_cost']:.2f}")
        col3.write(f"Ordered: {order['order_date']}")
        status_color = {"pending": "orange", "shipped": "blue", "delivered": "green", "cancelled": "red"}
        col4.write(f":{status_color.get(order['status'], 'gray')}[{order['status']}]")
else:
    st.info("No orders yet. Head to **Order Tracker** to log your first order.")

st.divider()

# --- Quick Start Guide ---
with st.expander("Quick Start Guide (click to expand)"):
    st.markdown("""
    ### How to use this suite:

    **1. Product Manager** (sidebar)
    - Add products you want to sell
    - Set source costs and selling prices
    - Track inventory levels
    - Use the pricing calculator to find optimal margins

    **2. Supplier Directory** (sidebar)
    - Browse pre-loaded suppliers across 4 niches
    - Add your own suppliers with MOQ, shipping, and reliability info
    - Compare suppliers side-by-side

    **3. Order Tracker** (sidebar)
    - Log orders to suppliers
    - Track shipping and delivery status
    - Monitor spending

    **4. Sales & Analytics** (sidebar)
    - Record sales from TikTok Shop
    - Track revenue, profit, and trends
    - See which products perform best

    ### Pricing Tips:
    - Aim for **60-80% margins** on TikTok Shop
    - Factor in **shipping, packaging, and TikTok fees (~5%)**
    - Price products in the **$15-$50 sweet spot** for impulse buys
    - Always order **samples first** before bulk ordering
    """)
