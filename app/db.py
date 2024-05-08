from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_rest_api.app.models.models import ProductModel, Base

engine = create_engine('sqlite:///const/products.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def connect():
    Base.metadata.create_all(engine)

def insert(product):
    session.add(product)
    session.commit()

def view():
    return session.query(ProductModel).all()

def get_product(id):
    return session.query(ProductModel).filter_by(id=id).first()

def update(product):
    existing_product = session.query(ProductModel).filter_by(id=product.id).first()
    if existing_product:
        existing_product.product_name = product.product_name
        existing_product.category = product.category
      #  existing_product.producer = product.producer
        existing_product.description = product.description
        existing_product.price = product.price
        session.commit()

def delete(id):
    product = session.query(ProductModel).filter_by(id=id).first()
    if product:
        session.delete(product)
        session.commit()

def deleteAll():
    session.query(ProductModel).delete()
    session.commit()
