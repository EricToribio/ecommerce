from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session


class Product:
    def __init__(self,data):
        self.id = data['id']
        self.price = data