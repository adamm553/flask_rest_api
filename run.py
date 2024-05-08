from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import ProductModel, Base, UserModel
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "SUPER-SECRET-KEY"
jwt = JWTManager(app)


engine = create_engine('sqlite:///products.db')
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

BASE_URL = '/products'

@app.route('/register', methods=["POST"])
def register():
    req_data = request.get_json()
    username = req_data.get('username')
    password = req_data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400
    
    existing_user = session.query(UserModel).filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400
    
    new_user = UserModel(username=username, password=password)
    session.add(new_user)
    session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    username = req_data.get('username')
    password = req_data.get("password")

    user = session.query(UserModel).filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Wrong username or password"}), 401
    

@app.route(BASE_URL, methods=["POST"])
@jwt_required()
def create_product():
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
@jwt_required()
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
@jwt_required
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

