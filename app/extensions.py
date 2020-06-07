from flask import Flask
from flask_mongoengine import MongoEngine

mongoengine = MongoEngine()

def init_app(app: Flask) -> None:
    mongoengine.init_app(app)
