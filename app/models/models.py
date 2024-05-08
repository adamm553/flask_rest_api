from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<UserModel(id=(self.id), username=(self.username))>"

class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<CategoryModel id: {self.id}, name: {self.name}>'

class ProductModel(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("CategoryModel")
   # producer = Column(String)
    description = Column(String)
    price = Column(Float)

    def __repr__(self):
        return f'<ProductModel id: {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category': self.category.name,  # Accessing category name via relationship
            #'producer': self.producer,
            'description': self.description,
            'price': self.price
        }
