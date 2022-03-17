from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["JWT_SECRET_KEY"] = "super-secret"
db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)

from doppelkopf import routes