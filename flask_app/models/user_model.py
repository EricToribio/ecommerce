from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session
from flask_app.models import addresses, shopping_cart
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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
        if request:=addresses.Address.get_address(check):
            address = request
        else:
            address = addresses.Address.add_address(check)
        cart = shopping_cart.Shopping_cart.new_cart()
    
        user_data = {
            **data,
            'address_id' : address.id,
            'shopping_cart_id':cart,
            'password':bcrypt.generate_password_hash(data['password'])
        }
        query = f"""INSERT INTO users ({', '.join(f'{key} 'for key in user_data)}) 
                            VALUES ({', '.join(f'%({key})s' for key in user_data)})"""
        
        print(user_data)
        results = connectToMySQL(DB).query_db(query,user_data)
        return results
    @classmethod
    def get_one(cls,**data):
        query = """SELECT * FROM users 
                    WHERE email = %(email)s;"""
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])

    @staticmethod
    def validate_new_user(data):
        errors = {}
        if 'email'in data and not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Please enter valid Email'
        elif 'email' in data and  User.get_one(email=data['email']):
            errors['email']='Please sign in email already has account'
        if 'password' in data and not  re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@!#$]{6,12}$", data['password']):
            errors['password'] = '''password requirements, one uppercase 
            letter, at least one lowercase letter, at least one special character'''
        elif 'password'in data and len(data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if 'password' in data and 'confirm_password' in data and data['password'] != data['confirm_password']:
            errors['confirm_password'] = 'Passwords do Not match'
        if 'first_name' in data and  len(data['first_name']) < 2:
            errors['first_name']='Please Enter valid First Name'
        if 'last_name' in data and len(data['last_name']) < 3:
            errors['last_name']='Please Enter valid Last Name'
        if 'street' in data and len(data['street']) < 5:
            errors['street']='Enter a valid street'
        if 'city' in data and len(data['city']) < 4:
            errors['city']='Enter a valid city'
        if 'state' in data and len(data['state']) < 3:
            errors['state']='Enter full State'
        if 'zip' in data and   len(data['zip']) < 5:
            errors['zip']='Enter a valid zip code'
        if 'username' in data and  len(data['username']) < 4:
            errors['username']='Username needs to be at least 4 characters'
        for category, message in errors.items():
            flash(message, category)
        return len(errors) == 0
