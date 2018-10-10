from flask import Flask
from flask_restful import Resource, Api
from flask_bootstrap import Bootstrap


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, **kwargs):
        kwargs["method"]="get"
        return kwargs

    def delete(self, **kwargs):
        kwargs["method"]="delete"
        return kwargs

    def post(self, **kwargs):
        kwargs["method"]="post"
        return kwargs

    def put(self, **kwargs):
        kwargs["method"]="put"
        return kwargs

class HelloWorld2(Resource):
    def get(self, **kwargs):
        kwargs["method"]="get"
        return kwargs

    def delete(self, **kwargs):
        kwargs["method"]="delete"
        return kwargs

    def post(self, **kwargs):
        kwargs["method"]="post"
        return kwargs

    def put(self, **kwargs):
        kwargs["method"]="put"
        return kwargs

api.add_resource(HelloWorld, '/api/exif/<string:xxhash>')
api.add_resource(HelloWorld2, '/api/xxhash/<string:path>')

if __name__ == '__main__':
    app.run(debug=True)
