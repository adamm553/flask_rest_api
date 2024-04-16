import sqlite3
import random
from app.product.models import ProductModel
from flask import jsonify

# def getNewId():
#     return random.getrandbits(28)

def commit_and_close_connection(conn):
    conn.commit()
    conn.close() 

def connect_to_database(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    return conn, cur 

def connect():
    conn, cur = connect_to_database('const/products.db')
    cur.execute("""CREATE TABLE IF NOT EXISTS products 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                category TEXT,
                producer TEXT,
                description TEXT,
                price FLOAT)""")
    
    try:
        cur.execute("ALTER TABLE products ADD COLUMN producer TEXT")
    except sqlite3.OperationalError as e:
        return jsonify({
            'res': "Can't create database",
            'status': '500'
         })
    
    commit_and_close_connection(conn)

def insert(product):
    conn, cur = connect_to_database('const/products.db')
    cur.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", (
        product.id,
        product.product_name,
        product.category,
        product.producer,
        product.description,
        product.price
    ))
    commit_and_close_connection(conn)

def view():
    conn, cur = connect_to_database('const/products.db')
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    products = []
    for row in rows:
        product = ProductModel(row[0], row[1], row[2], row[3], row[4], row[5])
        products.append(product)
    conn.close()
    return products

def get_product(id):
    conn, cur = connect_to_database('const/products.db')
    cur.execute("SELECT * FROM products where id=?", id)

def update(product):
    conn, cur = connect_to_database('const/products.db')
    cur.execute("UPDATE products SET product_name=?, category=?, producer=?, description=?, price=? WHERE id=?", (
        product.product_name,
        product.category,
        product.producer,
        product.description,
        product.price,
        product.id
    ))
    commit_and_close_connection(conn)

def delete(id):
    conn, cur = connect_to_database('const/products.db')
    cur.execute("DELETE FROM products WHERE id=?", (id, ))
    commit_and_close_connection(conn)

def deleteAll():
    conn, cur = connect_to_database('const/products.db')
    cur.execute("DELETE FROM products")
    commit_and_close_connection(conn)
