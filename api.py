from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}, 201

class TodoSimple(Resource):
    def get(self, todo_id):
        return {'hello': todo_id}, 201

    def post(self):
        return {'payload': request.get_json(force=True)}

api.add_resource(TodoSimple,
    '/todo/<string:todo_id>',
    '/todo'
)

api.add_resource(HelloWorld,
    '/',
    '/hello'
)

if __name__ == "__main__":
    app.run(debug=True)

"""
DESIGN DOC

General Overview

PHASE 1:
- Create a web application for sharing homemade cooked meals.
- As a user, I can create an account to the site, then make my own recipe.
- As a user, I can publish my own recipe or make it private
- As a user, my recipe can be peer reviewed and rated by other users
- As a user, I can review or bookmark someone's public recipe
- As a user, I can search a recipe using my available ingredients

PHASE 2:
- As as user, I


userTbl
- id, pk
- firstname
- lastname


cookeryuser / P@ssw0rd!

"""
