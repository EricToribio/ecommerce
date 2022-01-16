from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB,session
from flask_app.models import shopping_cart_products

class Orders:
    def __init__(self,data):
        self.id = data['id']
        self.user_order_id = data['user_order_id']
        self.total = data['total']/100
        self.created_at = data['created_at']

    @classmethod
    def add_order(cls,data):
        query = f'''INSERT INTO orders ({', '.join(f'{key} 'for key in data)})
                    VALUE ({', '.join(f'%({key})s 'for key in data)});'''
        results = connectToMySQL(DB).query_db(query,data)

        

        return results
    
    @classmethod
    def get_orders(cls,**data):
        query = """ SELECT * FROM orders 
                    WHERE user_order_id = %(user_order_id)s;"""

        results = connectToMySQL(DB).query_db(query,data)

        order = []
        if results:
            for row in results:
                order.append(cls(row))
        return order
