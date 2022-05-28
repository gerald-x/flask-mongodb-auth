from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from pathlib import Path
import os


up_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


app = Flask(__name__)
app.config.from_pyfile(f"{up_dir}/config.py")


db = MongoEngine(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


from . import views