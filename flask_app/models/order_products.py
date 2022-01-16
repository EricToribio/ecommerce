from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB,session

class Orders_products:
    def __init__(self,data):
        self.order_id = data['order_id']
        self.purchased_product_id = data['purchased_product_id']
        self.purchased_product_name = data['purchased_product_name']
        sel.purchased_product_description = data['purchased_product_description']

    @classmethod
    def add_item_to_order(cls,data):
        query = f""" INSERT INTO orders_has_products ({', '.join(f'{key} 'for key in data)})
                    VALUE ({', '.join(f'%({key})s 'for key in data)})"""

        results = connectToMySQL(DB).query_db(query,data)

        return results        