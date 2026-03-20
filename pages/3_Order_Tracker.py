"""Order Tracker — Track orders to suppliers."""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from datetime import date, timedelta
from database import get_products, add_order, get_orders, update_order_status

st.set_page_config(page_title="Order Tracker", page_icon="📋", layout="wide")
st.title("Order Tracker")
st.markdown("Track your supplier orders, shipping, and deliveries.")

# ==================== ADD ORDER ====================
st.subheader("Log New Order")
products = get_products()

if not products:
    st.warning("Add products in the **Product Manager** first.")
else:
    with st.form("add_order", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            product_options = {p["name"]: p["id"] for p in products}
            selected = st.selectbox("Product", list(product_options.keys()))
            quantity = st.number_input("Quantity", min_value=1, value=10, step=1)
            total_cost = st.number_input("Total Cost ($)", min_value=0.0, value=0.0, step=5.0)
        with col2:
            order_date = st.date_input("Order Date", value=date.today())
            expected_delivery = st.date_input("Expected Delivery", value=date.today() + timedelta(days=14))
            notes = st.text_input("Notes", placeholder="Tracking #, supplier contact, etc.")

        if st.form_submit_button("Log Order", type="primary"):
            add_order(product_options[selected], quantity, total_cost, str(order_date), str(expected_delivery), notes)
            st.success(f"Order logged: {quantity}x {selected}")
            st.rerun()

st.divider()

# ==================== ORDER LIST ====================
st.subheader("Your Orders")
orders = get_orders()

if orders:
    status_filter = st.selectbox("Filter", ["all", "pending", "shipped", "delivered", "cancelled"])
    filtered = orders if status_filter == "all" else [o for o in orders if o["status"] == status_filter]

    for order in filtered:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            col1.markdown(f"**{order['product_name'] or 'Unknown'}** — {order['quantity']} units")
            col2.caption(f"${order['total_cost']:.2f} | Ordered: {order['order_date']}")
            col3.caption(f"ETA: {order['expected_delivery']}")

            status_options = ["pending", "shipped", "delivered", "cancelled"]
            current_idx = status_options.index(order["status"]) if order["status"] in status_options else 0
            new_status = col4.selectbox(
                "Status", status_options, index=current_idx,
                key=f"order_status_{order['id']}", label_visibility="collapsed"
            )
            if new_status != order["status"]:
                update_order_status(order["id"], new_status)
                st.rerun()

            if order["notes"]:
                st.caption(f"Notes: {order['notes']}")

    st.divider()
    df = pd.DataFrame(orders)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", len(orders))
    col2.metric("Total Spent", f"${df['total_cost'].sum():,.2f}")
    col3.metric("Units Ordered", f"{df['quantity'].sum():,}")
else:
    st.info("No orders yet. Log your first order above!")
