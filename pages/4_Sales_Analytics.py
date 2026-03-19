"""Sales & Analytics — Track revenue and product performance."""

import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_products, add_sale, get_sales

st.set_page_config(page_title="Sales & Analytics", page_icon="📈", layout="wide")
st.title("Sales & Analytics")
st.markdown("Track your TikTok Shop sales and analyze product performance.")

# ==================== LOG SALE ====================
st.subheader("Log a Sale")
products = get_products()

if not products:
    st.warning("Add products in the **Product Manager** first.")
else:
    with st.form("add_sale", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_options = {p["name"]: p["id"] for p in products}
            selected = st.selectbox("Product", list(product_options.keys()))
        with col2:
            quantity = st.number_input("Quantity Sold", min_value=1, value=1, step=1)
            # Auto-calculate revenue from product price
            selected_product = next(p for p in products if p["name"] == selected)
            auto_revenue = selected_product["selling_price"] * quantity
            revenue = st.number_input("Revenue ($)", min_value=0.0, value=auto_revenue, step=1.0)
        with col3:
            platform = st.selectbox("Platform", ["tiktok_shop", "instagram", "website", "other"])

        if st.form_submit_button("Log Sale", type="primary"):
            add_sale(product_options[selected], quantity, revenue, platform)
            st.success(f"Sale logged: {quantity}x {selected} = ${revenue:.2f}")
            st.rerun()

st.divider()

# ==================== ANALYTICS ====================
sales = get_sales()

if sales:
    df = pd.DataFrame(sales)

    # Summary
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"{df['quantity'].sum():,}")
    col2.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")

    # Calculate profit
    product_costs = {p["name"]: p["source_cost"] for p in products}
    df["cost"] = df["product_name"].map(product_costs).fillna(0) * df["quantity"]
    total_profit = df["revenue"].sum() - df["cost"].sum()
    col3.metric("Total Profit", f"${total_profit:,.2f}")

    profit_margin = (total_profit / df["revenue"].sum() * 100) if df["revenue"].sum() > 0 else 0
    col4.metric("Profit Margin", f"{profit_margin:.1f}%")

    st.divider()

    # Charts
    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Product")
        rev_by_product = df.groupby("product_name")["revenue"].sum().reset_index()
        fig = px.bar(rev_by_product, x="product_name", y="revenue",
                     color_discrete_sequence=["#00f2ea"])
        fig.update_layout(xaxis_title="", yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Sales by Platform")
        platform_sales = df.groupby("platform")["quantity"].sum().reset_index()
        fig = px.pie(platform_sales, values="quantity", names="platform",
                     color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig, use_container_width=True)

    # Recent sales table
    st.divider()
    st.subheader("Recent Sales")
    display_df = df[["product_name", "quantity", "revenue", "platform", "sale_date"]].copy()
    display_df.columns = ["Product", "Qty", "Revenue", "Platform", "Date"]
    st.dataframe(display_df.head(20), use_container_width=True, hide_index=True)
else:
    st.info("No sales recorded yet. Log your first sale above!")

    st.divider()
    with st.expander("Tips for Your First Sales"):
        st.markdown("""
        ### Getting your first TikTok Shop sales:

        1. **Set up TikTok Shop** — Apply as a seller at seller-us.tiktok.com
        2. **List 3-5 products** — Start small, test what works
        3. **Price competitively** — Check what similar products sell for
        4. **Create content daily** — 2-3 videos per day minimum
        5. **Use TikTok Shop features** — Product links, live shopping, showcase

        ### Content that drives sales:
        - **Unboxing videos** — Show the product arriving
        - **Demo videos** — Show the product in action
        - **Before/After** — Dramatic transformations
        - **Customer reviews** — Share positive feedback
        - **Live selling** — TikTok LIVE with product showcase
        """)
