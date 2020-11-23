from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = MongoEngine()
db.init_app(app)
from application import routes