"""Product Manager — Add, price, and manage your TikTok Shop products."""

import streamlit as st
import pandas as pd
from database import add_product, get_products, update_product, delete_product

st.set_page_config(page_title="Product Manager", page_icon="📦", layout="wide")
st.title("Product Manager")
st.markdown("Source, price, and manage your product inventory.")

# ==================== ADD PRODUCT ====================
st.subheader("Add New Product")
with st.form("add_product", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Product Name *", placeholder="e.g., Resistance Band Set")
        niche = st.selectbox("Niche", [
            "Health & Fitness", "Home & Kitchen", "Beauty & Skincare",
            "Tech & Gadgets", "Fashion & Accessories", "Pet Products", "Other"
        ])
        source_cost = st.number_input("Source Cost ($)", min_value=0.0, value=0.0, step=0.50)
        selling_price = st.number_input("Selling Price ($)", min_value=0.0, value=0.0, step=1.0)

    with col2:
        supplier = st.text_input("Supplier", placeholder="e.g., CJ Dropshipping")
        moq = st.number_input("Min Order Quantity", min_value=1, value=1, step=1)
        inventory = st.number_input("Current Inventory", min_value=0, value=0, step=1)
        notes = st.text_area("Notes", placeholder="Sourcing details, product link, etc.", height=80)

    if st.form_submit_button("Add Product", type="primary"):
        if name:
            add_product(name, niche, source_cost, selling_price, supplier, moq, inventory, notes)
            st.success(f"Added **{name}**!")
            st.rerun()
        else:
            st.error("Product name is required.")

st.divider()

# ==================== PRICING CALCULATOR ====================
st.subheader("Pricing Calculator")
with st.expander("Calculate optimal pricing", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        calc_cost = st.number_input("Product Cost ($)", min_value=0.0, value=5.0, step=0.50, key="calc_cost")
        calc_shipping = st.number_input("Shipping Cost ($)", min_value=0.0, value=2.0, step=0.50, key="calc_ship")
        calc_packaging = st.number_input("Packaging Cost ($)", min_value=0.0, value=1.0, step=0.25, key="calc_pack")
    with col2:
        calc_tiktok_fee = st.number_input("TikTok Fee (%)", min_value=0.0, value=5.0, step=0.5, key="calc_fee")
        calc_target_margin = st.number_input("Target Margin (%)", min_value=0.0, value=70.0, step=5.0, key="calc_margin")

    total_cost = calc_cost + calc_shipping + calc_packaging
    if calc_target_margin < 100:
        suggested_price = total_cost / (1 - calc_target_margin / 100)
        tiktok_fee_amount = suggested_price * (calc_tiktok_fee / 100)
        actual_profit = suggested_price - total_cost - tiktok_fee_amount
        actual_margin = (actual_profit / suggested_price * 100) if suggested_price > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Cost", f"${total_cost:.2f}")
        col2.metric("Suggested Price", f"${suggested_price:.2f}")
        col3.metric("Profit per Unit", f"${actual_profit:.2f}")
        col4.metric("Actual Margin", f"{actual_margin:.1f}%")

        st.caption(f"TikTok fee: ${tiktok_fee_amount:.2f} per sale | Break-even at ${total_cost + tiktok_fee_amount:.2f}")

st.divider()

# ==================== PRODUCT LIST ====================
st.subheader("Your Products")
products = get_products()

if products:
    # Filter by niche
    niches = list(set(p["niche"] for p in products))
    niche_filter = st.selectbox("Filter by niche", ["All"] + sorted(niches))
    filtered = products if niche_filter == "All" else [p for p in products if p["niche"] == niche_filter]

    for product in filtered:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
            col1.markdown(f"**{product['name']}**")
            margin_color = "green" if product["margin_pct"] >= 60 else "orange" if product["margin_pct"] >= 40 else "red"
            col2.caption(f"Cost: ${product['source_cost']:.2f} → Sell: ${product['selling_price']:.2f} | :{margin_color}[{product['margin_pct']}% margin]")
            col3.caption(f"{product['niche']} | Stock: {product['inventory']} | MOQ: {product['moq']}")

            status_options = ["researching", "sampling", "active", "paused", "discontinued"]
            current_idx = status_options.index(product["status"]) if product["status"] in status_options else 0
            new_status = col4.selectbox(
                "Status", status_options, index=current_idx,
                key=f"status_{product['id']}", label_visibility="collapsed"
            )
            if new_status != product["status"]:
                update_product(product["id"], status=new_status)
                st.rerun()

            if col5.button("🗑️", key=f"del_{product['id']}"):
                delete_product(product["id"])
                st.rerun()

            if product["supplier"]:
                st.caption(f"Supplier: {product['supplier']}")
            if product["notes"]:
                st.caption(f"Notes: {product['notes']}")

    # Summary table
    st.divider()
    df = pd.DataFrame(filtered)
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Margin", f"{df['margin_pct'].mean():.1f}%")
    col2.metric("Total Inventory", f"{df['inventory'].sum():,}")
    col3.metric("Inventory Value", f"${(df['source_cost'] * df['inventory']).sum():,.2f}")
else:
    st.info("No products yet. Add your first product above!")
