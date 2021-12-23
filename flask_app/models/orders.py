from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB,session
from flask_app.models import shopping_cart_products

class Orders:
    def __init__(self,data):
        self.id = data['id']
        self.user_order_id = data['user_order_id']

    @classmethod
    def add_order(cls,data):
        query = f'INSERT INTO orders (user_order_id) VALUES (%({session["user_id"]})s;'
        results = connectToMySQL(DB).query_db(query)
        for row in data:
            product ={
            'purchased_product':data['product_id'],
            'order_id':results
            }
            order_products.Order_product.add_product(data)
            shopping_cart_products.Shopping_cart_product.delete()
            