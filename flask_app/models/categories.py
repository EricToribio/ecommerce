from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session
from flask_app.models import products

class Category:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']

    @property   
    def pro(self) :
        return products.Product.get_all(category_id = self.id)
        
        # else:
        #     return [1,2,3]
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM categories"
        results = connectToMySQL(DB).query_db(query)
        if results:
            cat = []
            for row in results:
                cat.append(cls(row))
            return cat
        

    @classmethod 
    def get_one(cls,data):
        query =f""" SELECT * FROM categories
                            WHERE {', '.join(f'{key} = %({key})s' for key in data)}"""
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])
            


    @classmethod
    def add_category(cls,data):
        query = 'INSERT INTO categories (name) VALUES (%(name)s)'
        results = connectToMySQL(DB).query_db(query,data)
        
