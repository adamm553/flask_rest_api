from flask import Flask 
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#klasa
class HelloWorld(Resource):
    def get(self, name, test):
        return {"name" : name, "test": test}
    

#dodanie klasy do strony
api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")

if __name__ == "__main__":
    app.run()