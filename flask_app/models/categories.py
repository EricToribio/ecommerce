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

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM categories"
        results = connectToMySQL(DB).query_db(query)
        if results:
            cat = []
            for row in results:
                cat.append(cls(row))
            return cat

    # @classmethod
    # def get_all(cls):
    #     query = """SELECT * FROM categories
    #                         JOIN products ON categories.id=products.category_id"""
    #     results = connectToMySQL(DB).query_db(query)
    #     if results:
    #         all_categories =[]
    #         for row in results:
    #             product_data = {
    #                 **row,
    #                 'id':row['products.id'],
    #                 'name':row['name'],
    #                 'created_at':row['created_at'],
    #                 'updated_at':row['updated_at']
    #             }
    #             cat = cls(row)
    #             cat.all_product=products.Product(product_data)
    #             all_categories.append(cat)
    #         return all_categories


    @classmethod 
    def get_one(cls,data):
        query =""" SELECT * FROM categories
                            WHERE name = %(name)s"""
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])
            


    @classmethod
    def add_category(cls,data):
        query = 'INSERT INTO categories (name) VALUES (%(name)s)'
        results = connectToMySQL(DB).query_db(query,data)
        
