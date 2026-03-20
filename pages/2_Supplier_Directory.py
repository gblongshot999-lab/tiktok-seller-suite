"""Supplier Directory — Find and manage product suppliers."""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from database import add_supplier, get_suppliers, delete_supplier

st.set_page_config(page_title="Supplier Directory", page_icon="🏭", layout="wide")
st.title("Supplier Directory")
st.markdown("Find reliable suppliers for your TikTok Shop products.")

# ==================== ADD SUPPLIER ====================
st.subheader("Add Supplier")
with st.form("add_supplier", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Supplier Name *", placeholder="e.g., CJ Dropshipping")
        platform = st.selectbox("Platform", [
            "CJ Dropshipping", "Alibaba", "AliExpress", "1688", "Temu (wholesale)",
            "US Warehouse", "Direct Manufacturer", "Other"
        ])
        niche = st.selectbox("Best For (Niche)", [
            "Health & Fitness", "Home & Kitchen", "Beauty & Skincare",
            "Tech & Gadgets", "All Niches", "Other"
        ])
        website = st.text_input("Website / Link", placeholder="https://...")
        contact = st.text_input("Contact Info", placeholder="Email, WhatsApp, etc.")

    with col2:
        moq = st.number_input("Min Order Quantity", min_value=1, value=1, step=1)
        shipping_speed = st.selectbox("Shipping Speed to US", [
            "3-7 days (US warehouse)", "7-15 days (ePacket/fast)",
            "15-30 days (standard)", "30-45 days (economy)", "Varies"
        ])
        reliability = st.slider("Reliability Rating", 1, 5, 3)
        certifications = st.text_input("Certifications", placeholder="e.g., FDA, CE, ISO")
        response_time = st.selectbox("Response Time", [
            "< 1 hour", "1-6 hours", "6-24 hours", "1-3 days", "Slow (3+ days)"
        ])
    notes = st.text_area("Notes", placeholder="Why this supplier? Special terms?", height=60)

    if st.form_submit_button("Add Supplier", type="primary"):
        if name:
            add_supplier(name, platform, niche, website, contact, moq, shipping_speed, reliability, certifications, response_time, notes)
            st.success(f"Added **{name}**!")
            st.rerun()
        else:
            st.error("Supplier name is required.")

st.divider()

# ==================== SUPPLIER LIST ====================
st.subheader("Your Suppliers")
suppliers = get_suppliers()

if suppliers:
    # Filters
    col1, col2 = st.columns(2)
    niche_filter = col1.selectbox("Filter by niche", ["All"] + sorted(set(s["niche"] for s in suppliers)))
    platform_filter = col2.selectbox("Filter by platform", ["All"] + sorted(set(s["platform"] for s in suppliers)))

    filtered = suppliers
    if niche_filter != "All":
        filtered = [s for s in filtered if s["niche"] == niche_filter]
    if platform_filter != "All":
        filtered = [s for s in filtered if s["platform"] == platform_filter]

    for supplier in filtered:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            stars = "⭐" * supplier["reliability"]
            col1.markdown(f"**{supplier['name']}** {stars}")
            col2.caption(f"{supplier['platform']} | {supplier['niche']}")
            col3.caption(f"MOQ: {supplier['moq']} | Ship: {supplier['shipping_speed']}")

            if col4.button("🗑️", key=f"del_sup_{supplier['id']}"):
                delete_supplier(supplier["id"])
                st.rerun()

            details = []
            if supplier["website"]:
                details.append(f"Website: {supplier['website']}")
            if supplier["contact"]:
                details.append(f"Contact: {supplier['contact']}")
            if supplier["certifications"]:
                details.append(f"Certs: {supplier['certifications']}")
            if supplier["response_time"]:
                details.append(f"Response: {supplier['response_time']}")
            if details:
                st.caption(" | ".join(details))
            if supplier["notes"]:
                st.caption(f"Notes: {supplier['notes']}")

    st.divider()
    st.subheader("Supplier Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Suppliers", len(filtered))
    avg_reliability = sum(s["reliability"] for s in filtered) / len(filtered) if filtered else 0
    col2.metric("Avg Reliability", f"{avg_reliability:.1f} / 5")
    col3.metric("Niches Covered", len(set(s["niche"] for s in filtered)))
else:
    st.info("No suppliers yet. Add one above or run the seed script to load starter suppliers!")
