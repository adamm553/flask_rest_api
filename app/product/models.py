class ProductModel:
    def __init__(self, id, product_name, category, producer, description, price):
        self.id = id
        self.product_name = product_name
        self.category = category
        self.producer = producer
        self.description = description
        self.price = price

    def __repr__(self):
        return '<ProductModel id: {}>'.format(self.id)
        
    def serialize(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category': self.category,
            'producer': self.producer,
            'description': self.description,
            'price': self.price
        }
