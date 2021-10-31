from flask import Flask
from flask_bs4 import Bootstrap
from .config import Config

def create_app():
    app = Flask(__name__)

    #Instanciamos boostrap con una instacia de flask
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)
    
    return app