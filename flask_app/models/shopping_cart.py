from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import  DB


class Shopping_cart:
    def __init__(self,data):
        self.id = data['id']

    @classmethod
    def new_cart(cls):
        query ='INSERT INTO shopping_cart() VALUES ()';

        results = connectToMySQL(DB).query_db(query)
        print(results)
        return results

    