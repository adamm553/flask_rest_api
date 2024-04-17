from flask import render_template, request, jsonify
import os, re, datetime
from app import db
from flask_rest_api.app.models.models import ProductModel
from run import app


BASE_URL = '/products'

if not os.path.isfile('products.db'):
    db.connect()

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False

@app.route(BASE_URL, methods=["POST"])
def postProduct():
   print('request: ', request)
   req_data = request.get_json()
   email = req_data['email']  
   if not isValid(email):
      return jsonify({
         'status': '422',
         'res': 'failure',
         'error': 'Invalid email format. Please enter a valid email address'
      })
   ############################
   product_name = req_data['product_name']
   category = req_data['category']
   producer = req_data['producer']
   description = req_data['description']
   price = req_data['price']
   prd = [p.serialize() for p in db.view()]
   for p in prd:
      if p['product_name'] == product_name:
         return jsonify({
            'res': 'Error, no such a product in the database',
            'status': '404'
         })
    #########################/\/\/\/\
   pr = ProductModel(db.getNewId(), product_name, category, producer, description, price)
   print('new product: ', pr.serialize())
   db.insert(pr)
   new_prd = [p.serialize() for p in db.view()]
   print('Products available: ', new_prd)

   return jsonify({
                # 'error': '',
                'res': pr.serialize(),
                'status': '200',
                'msg': 'New product added!!!'
            })


@app.route(BASE_URL, methods=['GET'])
def getProduct():
   content_type = request.headers.get('Content-Type')
   prd = [p.serialize() for p in db.view()]
   if content_type == 'application/json':
      json = request.json
      for p in prd:
         if p['id'] == int(json['id']):
            return jsonify({
                    # 'error': '',
                    'res': p,
                    'status': '200',
                    'msg': 'Products are being loaded'
                })
      return jsonify({
            'error': f"No product with id '{json['id']}'",
            'res': '',
            'status': '404'
        })
   else:
      return jsonify({
                  'res': prd,
                  'status': '200',
                  'msg': 'Products are being loaded',
                  'no_of_products': len(prd)
                })

@app.route(f"{BASE_URL}/<id>", methods=['GET'])
def getProductId(id):
   req_args = request.view_args
   prd = [p.serialize() for p in db.view()]
   if req_args:
      for p in prd:
         if p['id'] == int(req_args['id']):
            return jsonify({
                    # 'error': '',
                    'res': p,
                    'status': '200',
                    'msg': 'Success getting product by ID!'
                })
      return jsonify({
            'error': f"No product with id '{req_args['id']}'.",
            'res': '',
            'status': '404'
        })
   else:
      return jsonify({
                    # 'error': '',
                    'res': prd,
                    'status': '200',
                    'msg': 'Getting product by ID',
                    'no_of_products': len(prd)
                })

@app.route(BASE_URL, methods=['PUT'])
def putRequest():
   req_data = request.get_json()
   id = req_data['id']
   product_name = req_data['product_name']
   category = req_data['category']
   producer = req_data['producer']
   description = req_data['description']
   price = req_data['price']

   prd = [p.serialize() for p in db.view()]
   for p in prd:
      if p['id'] == id:
         pr = ProductModel(
            id,
            product_name,
            category,
            producer,
            description,
            price
         )
         print('New product: ', pr.serialize())
         db.update(pr)
         new_prd = [p.serialize() for p in db.view()]
         print('Products in stock', new_prd)
         return jsonify({
                # 'error': '',
                'res': pr.serialize(),
                'status': '200',
                'msg': f'Success updating the product named {product_name}!👍😀'
            })        
   return jsonify({
                # 'error': '',
                'res': f'Failed to update product with name: {product_name}!',
                'status': '404'
            })

@app.route(f"{BASE_URL}/<id>", methods=['DELETE'])
def deleteProduct(id):
   req_args = request.view_args
   prd = [p.serialize() for p in db.view()]
   if req_args:
      for p in prd:
         if p['id'] == int(req_args['id']):
            db.delete(p['id'])
            updated_prd = [p.serialize() for p in db.view()]
            print("Updated products: ", updated_prd)
            return jsonify({
                    'res': updated_prd,
                    'status': '200',
                    'msg': 'Success deleting product by ID!',
                    'no_of_products': len(updated_prd)
                })
   else:
      return jsonify({
            'error': f"No product ID sent!",
            'res': '',
            'status': '404'
        })
         