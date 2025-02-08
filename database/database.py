import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "prices.db")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id TEXT UNIQUE,
                        title TEXT,
                        price REAL,
                        old_price REAL,
                        availability TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')    
    
    # Following products
    c.execute('''CREATE TABLE IF NOT EXISTS tracked_products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id TEXT UNIQUE,
                        url TEXT NOT NULL
                    )''')
    
    conn.commit()
    conn.close()

def insert_or_update_product(product_id, title, price, availability):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
    result = c.fetchone()

    if result:
        old_price = result[0]
        c.execute("UPDATE products SET price = ?, old_price = ?, availability = ?, last_updated = CURRENT_TIMESTAMP WHERE product_id = ?", 
                           (price, old_price, availability, product_id))
        print(f"🔄 Product updated: {title} - New Price: {price} (Old: {old_price})")

    else:
        c.execute("INSERT INTO products (product_id, title, price, availability) VALUES (?, ?, ?, ?)", (product_id, title, price, availability))
        print(f"✅ New Product Added: {title} - Price: {price}")

    conn.commit()
    conn.close()

def add_tracked_product(product_id, url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO tracked_products (product_id, url) VALUES (?, ?)", (product_id, url))
    conn.commit()
    conn.close()
    print(f"✅ New product added to following list: {product_id}")

def get_tracked_products():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT product_id, url FROM tracked_products")
    products = c.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in products if len(row) == 2]