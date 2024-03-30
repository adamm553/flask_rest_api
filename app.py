from flask import Flask 
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

smartphones = {}


class Smartphone(Resource):
    def get(self, smartphone_id):
        return smartphones[smartphone_id]
    

api.add_resource(Smartphone, "/smartphone/<int:smartphone_id>")

if __name__ == "__main__":
    app.run()