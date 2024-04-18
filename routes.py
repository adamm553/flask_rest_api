from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models.models import UserModel, ProductModel
from sqlalchemy.orm import Session

user_routes = Blueprint('user_routes', __name__)
product_routes = Blueprint('product_routes', __name__)

@user_routes.route('/register', methods=["POST"])
def register(session: Session):
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

@user_routes.route('/login', methods=['POST'])
def login(session: Session):
    req_data = request.get_json()
    username = req_data.get('username')
    password = req_data.get("password")
    user = session.query(UserModel).filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Wrong username or password"}), 401

@product_routes.route('/products', methods=["POST"])
@jwt_required()
def post_product(session: Session):
    req_data = request.get_json()
    product_name = req_data['product_name']
    category = req_data['category']
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

@product_routes.route('/products', methods=['GET'])
@jwt_required()
def get_products(session: Session):
    products = session.query(ProductModel).all()
    return jsonify({
        'res': [product.serialize() for product in products],
        'status': '200',
        'msg': 'Products are being loaded',
        'no_of_products': len(products)
    })

@product_routes.route('/products/<int:id>', methods=['GET'])
def get_product(session: Session, id):
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

@product_routes.route('/products', methods=['PUT'])
def put_product(session: Session):
    req_data = request.get_json()
    id = req_data['id']
    product_name = req_data['product_name']
    category = req_data['category']
    description = req_data['description']
    price = req_data['price']
    product = session.query(ProductModel).filter_by(id=id).first()
    if product:
        product.product_name = product_name
        product.category = category
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

@product_routes.route('/products/<int:id>', methods=['DELETE'])
@jwt_required
def delete_product(session: Session, id):
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
