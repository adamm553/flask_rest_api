from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)
   # producer = Column(String)  # Add the producer column here
    description = Column(String)
    price = Column(Float)

    def __repr__(self):
        return f'<ProductModel id: {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category': self.category,
            #'producer': self.producer,
            'description': self.description,
            'price': self.price
        }
