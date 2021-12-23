from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session
from flask_app.models import categories,user_model

class Product:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.picture = data['picture']
        self.description = data['description']
        self.quantity = data['quantity']
        self.on_sale = data['on_sale']
        self.name = data['name']
        self.user_id = data['user_id']
        self.category_id = data['category_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    

    @property
    def cat(self):
        data = {
            "id":self.category_id
        }
        return categories.Category.get_one(**data)


    @classmethod
    def add_product(cls,data):
        cat ={
            'name' : data['category_id'].lower()
        }
        check = categories.Category.get_one(name=data['category_id'].lower())
        if not check:
            categories.Category.add_category(cat)

        category =categories.Category.get_one(name=data['category_id'].lower())

        product_data = {
            **data,
            'category_id': category.id,
            'picture':f"{session['user_id']}_{data['name']}"
        }
        query = f"""INSERT INTO products ({', '.join(f'{key}' for key in product_data)})
                            VALUES ({', '.join(f'%({key})s'for key in product_data)});"""
        results = connectToMySQL(DB).query_db(query, product_data)
        if results:
            return results 

    @classmethod
    def get_all(cls,**data) -> list:
        query  = f"""SELECT * FROM products
                            WHERE category_id =%(category_id)s
                            LIMIT 5;"""

        results = connectToMySQL(DB).query_db(query,data)
        print(results)
        pro = []
        if results:
            for row in results:
                pro.append(cls(row))
            print('get all products')
        return pro
    @classmethod
    def get_user_products(cls,**data):
        query = f""" SELECT * FROM products 
                        WHERE {', '.join(f'{key} = %({key})s' for key in data )} ;"""
        results = connectToMySQL(DB).query_db(query,data)
        pro = []

        if results:
            for row in results:
                pro.append(cls(row))
            print('get all products')
        return pro

    @classmethod
    def get_one(cls,**data):
        query = """SELECT * FROM products 
                            WHERE products.id = %(id)s;"""

        results = connectToMySQL(DB).query_db(query,data)

        if results:
            return cls(results[0])

    @classmethod
    def get_products_cart(cls,**data):
        query = """SELECT * FROM products  
                            JOIN shopping_cart_products on product_id = products.id 
                        WHERE shopping_cart_id = %(shopping_cart_id)s;"""
        results = connectToMySQL(DB).query_db(query,data)
        pro = []
        if results:
            for row in results:
                pro.append(cls(row))
            print('get all products')
        return pro