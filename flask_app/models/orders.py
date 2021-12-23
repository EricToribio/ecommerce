from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB,session
from flask_app.models import shopping_cart_products

class Orders:
    def __init__(self,data):
        self.id = data['id']
        self.user_order_id = data['user_order_id']
        self.created_at = data['created_at']

    @classmethod
    def add_order(cls):
        query = f'INSERT INTO orders (user_order_id) VALUES (%({session["user_id"]})s;'
        results = connectToMySQL(DB).query_db(query)
        return results
    
    @classmethod
    def get_orders(cls,data):
        query - """ SELECT * FROM orders 
                            JOIN orders_has_products ON orders.id = order_id
                            JOIN products ON products.id = orders_has_products.purchased_product_id
                            where user_order_id = %(user_order_id)s;"""

        results - connectToMySQL(DB).query_db(query,data)

    orders = []
    if results:
        for row in results:
            pass
            
