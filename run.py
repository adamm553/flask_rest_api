from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.product.models import ProductModel, Base

app = Flask(__name__)
engine = create_engine('sqlite:///products.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

BASE_URL = '/products'

@app.route(BASE_URL, methods=["POST"])
def post_product():
    req_data = request.get_json()
    product_name = req_data['product_name']
    category = req_data['category']
    #producer = req_data['producer']
    description = req_data['description']
    price = req_data['price']

    existing_product = session.query(ProductModel).filter_by(product_name=product_name).first()
    if existing_product:
        return jsonify({
            'res': 'Error, a product with the same name already exists',
            'status': '404'
        })

    new_product = ProductModel(
        product_name=product_name,
        category=category,
       # producer=producer,
        description=description,
        price=price
    )
    session.add(new_product)
    session.commit()

    return jsonify({
        'res': new_product.serialize(),
        'status': '201',
        'msg': 'New product added!!!'
    })

@app.route(BASE_URL, methods=['GET'])
def get_products():
    products = session.query(ProductModel).all()
    return jsonify({
        'res': [product.serialize() for product in products],
        'status': '200',
        'msg': 'Products are being loaded',
        'no_of_products': len(products)
    })

@app.route(f"{BASE_URL}/<int:id>", methods=['GET'])
def get_product(id):
    product = session.query(ProductModel).filter_by(id=id).first()
    if product:
        return jsonify({
            'res': product.serialize(),
            'status': '200',
            'msg': 'Success getting product by ID!'
        })
    else:
        return jsonify({
            'error': f"No product with id '{id}'",
            'res': '',
            'status': '404'
        })

@app.route(BASE_URL, methods=['PUT'])
def put_product():
    req_data = request.get_json()
    id = req_data['id']
    product_name = req_data['product_name']
    category = req_data['category']
    #producer = req_data['producer']
    description = req_data['description']
    price = req_data['price']

    product = session.query(ProductModel).filter_by(id=id).first()
    if product:
        product.product_name = product_name
        product.category = category
       # product.producer = producer
        product.description = description
        product.price = price
        session.commit()
        return jsonify({
            'res': product.serialize(),
            'status': '200',
            'msg': f'Success updating the product named {product_name}!'
        })
    else:
        return jsonify({
            'error': f"No product with id '{id}'",
            'res': '',
            'status': '404'
        })

@app.route(f"{BASE_URL}/<int:id>", methods=['DELETE'])
def delete_product(id):
    product = session.query(ProductModel).filter_by(id=id).first()
    if product:
        session.delete(product)
        session.commit()
        return jsonify({
            'res': f'Success deleting product with ID {id}!',
            'status': '200',
            'msg': 'Product deleted!'
        })
    else:
        return jsonify({
            'error': f"No product with id '{id}'",
            'res': '',
            'status': '404'
        })

if __name__ == '__main__':
    app.run()
