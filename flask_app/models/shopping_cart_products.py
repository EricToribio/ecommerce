from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import  DB
from flask_app.models import products


class Shopping_cart_product:
    def __init__(self,data):
        self.product_id = data['product_id']
        self.shopping_cart_id =data['shopping_cart_id']

    # @property
    # def products(self):
    #     return products.Product.get_all(id=self.product_id)

    @classmethod
    def add_to_cart(self,data):
        query = """ INSERT  INTO shopping_cart_products (product_id, shopping_cart_id)
                            VALUES ( %(product_id)s , %(shopping_cart_id)s)"""
        results = connectToMySQL(DB).query_db(query,data)

        return results

    @classmethod
    def get_product_in_cart(self,**data) -> list:
        query = """ SELECT * FROM shopping_cart_products 
                            JOIN products ON products.id = product_id
                            WHERE shopping_cart_id = %(shopping_cart_id)s;"""
        results = connectToMySQL(DB).query_db(query,data)

        product = []
        if results:
            for row in results:
                product.append(products.Product(row))
        
        return products

    @classmethod
    def delete_item(self,data):
        query = """ Delete FROM shopping_cart_products
                WHERE product_id = %(product_id)s 
                AND shopping_cart_id = %(shopping_cart_id)s
                LIMIT 1;"""

        results = connectToMySQL(DB).query_db(query,data)

    
