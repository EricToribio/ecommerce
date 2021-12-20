from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session


class Product:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.picture = data['picture']
        self.description = data['description']
        self.quantity = data['quantity']
        self.on_sale = data['on_sale']
        self.name = data['name']
        self.category_id = data['category_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
