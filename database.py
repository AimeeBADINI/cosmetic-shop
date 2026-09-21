import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "boutique.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'vendeur',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 5,
            barcode TEXT UNIQUE,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            loyalty_points INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            user_id INTEGER,
            total REAL NOT NULL,
            payment_method TEXT DEFAULT 'espèces',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Sale items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Default admin user (password: admin123)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            ("admin", "admin123", "Administrateur", "admin")
        )
        # Sample products
        sample_products = [
            ("Rouge à lèvres Matte", "Maybelline", "Maquillage", 12.99, 50, 10, "LIP001", "Rouge longue tenue"),
            ("Crème hydratante visage", "Nivea", "Soin", 9.50, 30, 5, "CRE001", "Hydratation 24h"),
            ("Mascara Volume", "L'Oréal", "Maquillage", 14.99, 40, 8, "MAS001", "Volume extrême"),
            ("Fond de teint liquide", "Maybelline", "Maquillage", 18.50, 25, 5, "FON001", "Couverture naturelle"),
            ("Sérum vitamine C", "The Ordinary", "Soin", 22.00, 20, 5, "SER001", "Éclat et anti-âge"),
            ("Vernis à ongles", "Essie", "Ongles", 8.99, 60, 10, "VER001", "Couleurs tendances"),
            ("Parfum eau de toilette", "Chanel", "Parfum", 89.00, 15, 3, "PAR001", "Senteur florale"),
            ("Shampoing réparateur", "L'Oréal", "Cheveux", 11.50, 35, 8, "SHA001", "Répare les cheveux abîmés"),
        ]
        cursor.executemany(
            "INSERT INTO products (name, brand, category, price, stock, min_stock, barcode, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            sample_products
        )

    conn.commit()
    conn.close()


# ---------- Users ----------
def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, role, created_at FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users


# ---------- Products ----------
def get_all_products(search=None, category=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    if search:
        query += " AND (name LIKE ? OR brand LIKE ? OR barcode LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s])
    if category and category != "Toutes":
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY name"
    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products


def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return dict(product) if product else None


def add_product(name, brand, category, price, stock, min_stock, barcode, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO products (name, brand, category, price, stock, min_stock, barcode, description, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, brand, category, price, stock, min_stock, barcode or None, description, datetime.now().isoformat())
        )
        conn.commit()
        pid = cursor.lastrowid
        conn.close()
        return pid
    except sqlite3.IntegrityError:
        conn.close()
        return None


def update_product(product_id, name, brand, category, price, stock, min_stock, barcode, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE products SET name=?, brand=?, category=?, price=?, stock=?, min_stock=?,
               barcode=?, description=?, updated_at=? WHERE id=?""",
            (name, brand, category, price, stock, min_stock, barcode or None, description,
             datetime.now().isoformat(), product_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category")
    cats = [row[0] for row in cursor.fetchall()]
    conn.close()
    return cats


def get_low_stock_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE stock <= min_stock ORDER BY stock")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products


# ---------- Customers ----------
def get_all_customers(search=None):
    conn = get_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute(
            "SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY name",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cursor.execute("SELECT * FROM customers ORDER BY name")
    customers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return customers


def add_customer(name, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
        (name, phone, email, address)
    )
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid


def update_customer(customer_id, name, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
        (name, phone, email, address, customer_id)
    )
    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()


# ---------- Sales ----------
def create_sale(customer_id, user_id, items, payment_method="espèces", notes=""):
    """
    items: list of dicts {product_id, quantity, unit_price}
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        total = sum(item["quantity"] * item["unit_price"] for item in items)
        cursor.execute(
            "INSERT INTO sales (customer_id, user_id, total, payment_method, notes) VALUES (?, ?, ?, ?, ?)",
            (customer_id, user_id, total, payment_method, notes)
        )
        sale_id = cursor.lastrowid

        for item in items:
            subtotal = item["quantity"] * item["unit_price"]
            cursor.execute(
                "INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)",
                (sale_id, item["product_id"], item["quantity"], item["unit_price"], subtotal)
            )
            # Update stock
            cursor.execute(
                "UPDATE products SET stock = stock - ?, updated_at = ? WHERE id = ?",
                (item["quantity"], datetime.now().isoformat(), item["product_id"])
            )

        conn.commit()
        conn.close()
        return sale_id
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e


def get_sales(limit=50, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT s.*, c.name as customer_name, u.full_name as seller_name
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN users u ON s.user_id = u.id
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND date(s.created_at) >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date(s.created_at) <= ?"
        params.append(end_date)
    query += " ORDER BY s.created_at DESC LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    sales = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sales


def get_sale_details(sale_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.*, c.name as customer_name, u.full_name as seller_name
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN users u ON s.user_id = u.id
        WHERE s.id = ?
    """, (sale_id,))
    sale = cursor.fetchone()
    if not sale:
        conn.close()
        return None
    sale = dict(sale)
    cursor.execute("""
        SELECT si.*, p.name as product_name, p.brand
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
    """, (sale_id,))
    sale["items"] = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sale


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # Total products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Low stock
    cursor.execute("SELECT COUNT(*) FROM products WHERE stock <= min_stock")
    low_stock = cursor.fetchone()[0]

    # Total customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    # Sales today
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(total), 0) FROM sales WHERE date(created_at) = ?", (today,))
    sales_today_count, sales_today_total = cursor.fetchone()

    # Sales this month
    month = datetime.now().strftime("%Y-%m")
    cursor.execute(
        "SELECT COUNT(*), COALESCE(SUM(total), 0) FROM sales WHERE strftime('%Y-%m', created_at) = ?",
        (month,)
    )
    sales_month_count, sales_month_total = cursor.fetchone()

    # Total revenue
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM sales")
    total_revenue = cursor.fetchone()[0]

    conn.close()
    return {
        "total_products": total_products,
        "low_stock": low_stock,
        "total_customers": total_customers,
        "sales_today_count": sales_today_count,
        "sales_today_total": sales_today_total,
        "sales_month_count": sales_month_count,
        "sales_month_total": sales_month_total,
        "total_revenue": total_revenue,
    }
