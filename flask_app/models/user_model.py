from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session
from flask_app.models import addresses, shopping_cart
from flask_app.models import products





# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username =data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address_id = data['address_id']
        self.shopping_cart_id = data['shopping_cart_id']

    @property
    def full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    @property
    def user_products(self):
        return products.Product.get_user_products(user_id = self.id)

    def __repr__(self):
        return f"< first name: {self.first_name}, id:{self.id} > "
    # Now we use class methods to query our database
    
    
    @classmethod
    def add_user(cls,data):
        check = {
            'street' : data['street'],
            'city': data['city'],
            'state':data['state'],
            'zip':data['zip']
        }
        request = addresses.Address.get_address(check)
        if not request:
            insert = addresses.Address.add_address(check)
        
        address = addresses.Address.get_address(check)
        cart = shopping_cart.Shopping_cart.new_cart()
        user_data = {
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'username':data['username'],
            'email':data['email'],
            'address_id' : address.id,
            'shopping_cart_id':cart,
            'password':bcrypt.generate_password_hash(data['password'])
        }
        query = f"""INSERT INTO users ({', '.join(f'{key} 'for key in user_data)}) 
                            VALUES ({', '.join(f'%({key})s' for key in user_data)})"""
        
        print(user_data)
        results = connectToMySQL(DB).query_db(query,user_data)
        if results:
            return results

    @classmethod
    def get_one_join(cls,**data):
        query = f"""SELECT * FROM users 
                        JOIN addresses ON addresses.id=users.address_id
                    WHERE {'and '.join(f'users.{key} = %({key})s' for key in data)}"""
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            user = cls(results[0])
            user.address = []
            for row in results:
                address_data ={
                    **row,
                    "id":row['addresses.id'],
                    "created_at":row['addresses.created_at'],
                    "updated_at":row['addresses.updated_at']
                }
            user.address.append(addresses.Address(address_data))
            return user
    
    @classmethod
    def get_one(cls,**data):
        query = f"""SELECT * FROM users 
        WHERE {'and '.join(f'users.{key} = %({key})s' for key in data)}"""

        results = connectToMySQL(DB).query_db(query,data)

        if results:
            return cls(results[0])

    @classmethod
    def update_user(cls, data):
        print(data)
        check = {
            'id':data['id'],
            'street' : data['street'],
            'city': data['city'],
            'state':data['state'],
            'zip':data['zip']
        }
        
        
        addresses.Address.update_address(check )

        user_data = {
            'id':session['user_id'],
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'username':data['username'],
            'email':data['email']
        }
        query = """UPDATE users SET first_name =%(first_name)s, last_name = %(last_name)s,username =%(username)s,email=%(email)s
                            WHERE id = %(id)s;"""

        results = connectToMySQL(DB).query_db(query,user_data)


