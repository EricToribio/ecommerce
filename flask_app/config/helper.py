from functools import wraps
from flask import flash, session, redirect,flash,request
from flask_app.models.user_model import User,EMAIL_REGEX
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/')
        return view(*args, **kwargs)
    return inner


def new_user_validation(func):
    @wraps(func)
    def inner(*args,**kwargs):
        data ={
            **request.form
        }
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
    return inner


# def update_user_account(cls,data):
#     # data ={
#     #     **request.form
#     # }
#     errors = {}
#     if 'email'in data and not EMAIL_REGEX.match(data['email']):
#         errors['email'] = 'Please enter valid Email'
#     # elif 'email' in data and  User.get_one(email=data['email']):
#     #     errors['email']='Please sign in email already has account'
#     if 'password' in data and not  re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@!#$]{6,12}$", data['password']):
#         errors['password'] = '''password requirements, one uppercase 
#         letter, at least one lowercase letter, at least one special character'''
#     elif 'password'in data and len(data['password']) < 8:
#         errors['password'] = 'Password must be at least 8 characters long'
#     if 'password' in data and 'confirm_password' in data and data['password'] != data['confirm_password']:
#         errors['confirm_password'] = 'Passwords do Not match'
#     if 'first_name' in data and  len(data['first_name']) < 2:
#         errors['first_name']='Please Enter valid First Name'
#     if 'last_name' in data and len(data['last_name']) < 3:
#         errors['last_name']='Please Enter valid Last Name'
#     if 'street' in data and len(data['street']) < 5:
#         errors['street']='Enter a valid street'
#     if 'city' in data and len(data['city']) < 4:
#         errors['city']='Enter a valid city'
#     if 'state' in data and len(data['state']) < 3:
#         errors['state']='Enter full State'
#     if 'zip' in data and   len(data['zip']) < 5:
#         errors['zip']='Enter a valid zip code'
#     if 'username' in data and  len(data['username']) < 4:
#         errors['username']='Username needs to be at least 4 characters'
#     for category, message in errors.items():
#         flash(message, category)
#     return len(errors) == 0
  
