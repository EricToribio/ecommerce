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


    @classmethod
    def add_product(cls,data):
        cat ={
            'name' : data['category_id'].lower()
        }
        check = categories.Category.get_one(cat)
        if not check:
            categories.Category.add_category(cat)

        category =categories.Category.get_one(cat)

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
    def get_all(cls,**data):
        query  = """SELECT * FROM products
                            WHERE category_id =%(category_id)s"""

        results = connectToMySQL(DB).query_db(query,data)
        if results:
            pro = []
            for row in results:
                pro.append(cls(row))
            return pro
        #     all_products =[]
        #     for row in results:
        #         user_data ={
        #             **row,
        #             'id': row['users.id'],
        #             "created_at":row['users.created_at'],
        #             "updated_at":row['users.updated_at']
        #                 }
        #         categories_data = {
        #             'id':row['categories.id'],
        #             "name":row['categories.name']
        #         }
        #         product = cls(row)
        #         product.user=user_model.User(user_data)
        #         product.category = categories.Category(categories_data)
        #         all_products.append(product)
        # return all_products

    @classmethod
    def get_one(cls,**data):
        query = """SELECT * FROM products 
                        JOIN categories ON categories.id=products.category_id
                            WHERE products.id = %(id)s;"""

        results = connectToMySQL(DB).query_db(query,data)

        if results:
            one_product = []
            for row in results:
                cat_data = {
                    **row,
                    'id':row['categories.id'],
                    'name':row['categories.name']
                }
                pro=cls(row)
                pro.cat=categories.Category(cat_data)
                one_product.append(pro)
            return one_product