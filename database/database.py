import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "prices.db")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id TEXT UNIQUE,
                        platform TEXT NOT NULL,
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
                        platform TEXT NOT NULL,
                        url TEXT NOT NULL
                    )''')
    
    conn.commit()
    conn.close()

def insert_or_update_product(product_id, platform, title, price, availability):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute("SELECT COUNT(*) FROM products WHERE product_id = ?", (product_id,))
        exists = c.fetchone()[0]

        if exists == 0:
            print(f"🛠 New Product Adding: {product_id} - {title} ({price} €) - {availability}")
            c.execute("INSERT INTO products (product_id, platform, title, price, old_price, availability) VALUES (?, ?, ?, ?, ?, ?)",
                           (product_id, platform, title, price, price, availability))
        else:
            print(f"🔄 Product Updating: {product_id} - {title} ({price} €) - {availability}")
            c.execute("UPDATE products SET title = ?, price = ?, old_price = price, availability = ? WHERE product_id = ?",
                           (title, price, availability, product_id))

        conn.commit()
    except Exception as e:
        print(f"❌ DB write error: {e}")
    finally:
        conn.close()

def add_tracked_product(product_id, platform, url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO tracked_products (product_id, platform, url) VALUES (?, ?, ?)", 
              (product_id, platform, url))
    c.execute("SELECT COUNT(*) FROM products WHERE product_id = ?", (product_id,))
    exists = c.fetchone()[0]
    conn.commit()
    conn.close()
    print(f"✅ New product added to following list: {product_id}")

def get_tracked_products():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT product_id, platform, url FROM tracked_products")
    products = c.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in products if len(row) == 2]

def check_price_drop(product_id, new_price):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
    result = c.fetchone()

    conn.close()

    if result:
        old_price = result[0]
        if old_price > new_price:
            print(f"📉 Price Dropped! {old_price} € → {new_price} €")
            return True
    return False