from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# from flask_cors import CORS

from settings import *
from routes import initialize_routes

from db import db

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

api = Api(app)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
# cors = CORS(app, resources={r"/v1/*": {"origins": "*"}, r"/v1/dish/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_routes(api)
db.init_app(app)

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    initialize_routes(api)
    app.run(port=5000, debug=True)
