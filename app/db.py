import sqlite3
import random
from app.product.models import ProductModel

def getNewId():
    return random.getrandbits(28)

def connect():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS products 
                (id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                producer TEXT,
                description TEXT,
                price FLOAT)""")
    
    # Dodaj kolumnę 'producer', jeśli jeszcze jej nie ma
    try:
        cur.execute("ALTER TABLE products ADD COLUMN producer TEXT")
    except sqlite3.OperationalError as e:
        # Jeśli kolumna już istnieje, zignoruj błąd
        pass
    
    conn.commit()
    conn.close()

def insert(product):
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", (
        product.id,
        product.product_name,
        product.category,
        product.producer,
        product.description,
        product.price
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    products = []
    for row in rows:
        product = ProductModel(row[0], row[1], row[2], row[3], row[4], row[5])
        products.append(product)
    conn.close()
    return products

def update(product):
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("UPDATE products SET product_name=?, category=?, producer=?, description=?, price=? WHERE id=?", (
        product.product_name,
        product.category,
        product.producer,
        product.description,
        product.price,
        product.id
    ))
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (id, ))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM products")
    conn.commit()
    conn.close()
