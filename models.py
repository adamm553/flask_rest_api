from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class DeviceModel(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String())
    category = db.Column(db.String())
    producer = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float)

    def __init__(self, product_name, category, producer, description, price):
        self.product_name = product_name
        self.category = category
        self.producer = producer
        self.description = description
        self.price = price

        def __repr__(self):
            return f"{self.product_name}:{self.price}"