"""Database module for TikTok Seller Suite — SQLite storage."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "seller.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            niche TEXT,
            source_cost REAL DEFAULT 0.0,
            selling_price REAL DEFAULT 0.0,
            margin_pct REAL DEFAULT 0.0,
            supplier TEXT,
            moq INTEGER DEFAULT 1,
            inventory INTEGER DEFAULT 0,
            status TEXT DEFAULT 'researching',
            notes TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            platform TEXT,
            niche TEXT,
            website TEXT,
            contact TEXT,
            moq INTEGER DEFAULT 1,
            shipping_speed TEXT,
            reliability INTEGER DEFAULT 3,
            certifications TEXT,
            response_time TEXT,
            notes TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER DEFAULT 0,
            total_cost REAL DEFAULT 0.0,
            order_date TEXT,
            expected_delivery TEXT,
            status TEXT DEFAULT 'pending',
            tracking TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            revenue REAL DEFAULT 0.0,
            platform TEXT DEFAULT 'tiktok_shop',
            sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


# --- Product CRUD ---

def add_product(name, niche, source_cost, selling_price, supplier="", moq=1, inventory=0, notes=""):
    margin_pct = ((selling_price - source_cost) / selling_price * 100) if selling_price > 0 else 0
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, niche, source_cost, selling_price, margin_pct, supplier, moq, inventory, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, niche, source_cost, selling_price, round(margin_pct, 1), supplier, moq, inventory, notes),
    )
    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_product(product_id, **kwargs):
    conn = get_connection()
    for key, value in kwargs.items():
        conn.execute(f"UPDATE products SET {key} = ? WHERE id = ?", (value, product_id))
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


# --- Supplier CRUD ---

def add_supplier(name, platform, niche, website="", contact="", moq=1, shipping_speed="", reliability=3, certifications="", response_time="", notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO suppliers (name, platform, niche, website, contact, moq, shipping_speed, reliability, certifications, response_time, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, platform, niche, website, contact, moq, shipping_speed, reliability, certifications, response_time, notes),
    )
    conn.commit()
    conn.close()


def get_suppliers():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM suppliers ORDER BY reliability DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_supplier(supplier_id):
    conn = get_connection()
    conn.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
    conn.commit()
    conn.close()


# --- Order CRUD ---

def add_order(product_id, quantity, total_cost, order_date, expected_delivery, notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO orders (product_id, quantity, total_cost, order_date, expected_delivery, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (product_id, quantity, total_cost, order_date, expected_delivery, notes),
    )
    conn.commit()
    conn.close()


def get_orders():
    conn = get_connection()
    rows = conn.execute("""
        SELECT o.*, p.name as product_name
        FROM orders o
        LEFT JOIN products p ON o.product_id = p.id
        ORDER BY o.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_order_status(order_id, status):
    conn = get_connection()
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()


# --- Sales CRUD ---

def add_sale(product_id, quantity, revenue, platform="tiktok_shop"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO sales (product_id, quantity, revenue, platform) VALUES (?, ?, ?, ?)",
        (product_id, quantity, revenue, platform),
    )
    conn.commit()
    conn.close()


def get_sales():
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.*, p.name as product_name
        FROM sales s
        LEFT JOIN products p ON s.product_id = p.id
        ORDER BY s.sale_date DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Analytics ---

def get_dashboard_stats():
    conn = get_connection()
    stats = {}
    stats["total_products"] = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    stats["active_products"] = conn.execute("SELECT COUNT(*) FROM products WHERE status = 'active'").fetchone()[0]
    stats["total_inventory"] = conn.execute("SELECT COALESCE(SUM(inventory), 0) FROM products").fetchone()[0]
    stats["total_suppliers"] = conn.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0]
    stats["total_revenue"] = conn.execute("SELECT COALESCE(SUM(revenue), 0) FROM sales").fetchone()[0]
    stats["total_sales"] = conn.execute("SELECT COALESCE(SUM(quantity), 0) FROM sales").fetchone()[0]
    stats["pending_orders"] = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0]
    stats["total_cost"] = conn.execute("SELECT COALESCE(SUM(total_cost), 0) FROM orders").fetchone()[0]
    conn.close()
    return stats


# Initialize on import
init_db()
