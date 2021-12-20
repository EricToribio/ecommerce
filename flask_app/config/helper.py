from functools import wraps
from flask import flash, session, redirect,flash,request
from flask_app.models.user_model import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/')
        return view(*args, **kwargs)
    return inner



def new_user_validation(*args,**kwargs):
    errors = {}
    print(request.form)
    if 'email'in request.form and not EMAIL_REGEX.match(request.form['email']):
        errors['email'] = 'Please enter valid Email'
    elif 'email' in request.form and  User.get_one(email=request.form['email']):
        errors['email']='Please sign in email already has account'
    if 'password' in request.form and not  re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@!#$]{6,12}$", request.form['password']):
        errors['password'] = '''password requirements, one uppercase 
        letter, at least one lowercase letter, at least one special character'''
    elif 'password'in request.form and len(request.form['password']) < 8:
        errors['password'] = 'Password must be at least 8 characters long'
    if 'password' in request.form and 'confirm_password' in request.form and request.form['password'] != request.form['confirm_password']:
        errors['confirm_password'] = 'Passwords do Not match'
    if 'first_name' in request.form and  len(request.form['first_name']) < 2:
        errors['first_name']='Please Enter valid First Name'
    if 'last_name' in request.form and len(request.form['last_name']) < 3:
        errors['last_name']='Please Enter valid Last Name'
    if 'street' in request.form and len(request.form['street']) < 5:
        errors['street']='Enter a valid street'
    if 'city' in request.form and len(request.form['city']) < 4:
        errors['city']='Enter a valid city'
    if 'state' in request.form and len(request.form['state']) < 3:
        errors['state']='Enter full State'
    if 'zip' in request.form and   len(request.form['zip']) < 5:
        errors['zip']='Enter a valid zip code'
    if 'username' in request.form and  len(request.form['username']) < 4:
        errors['username']='Username needs to be at least 4 characters'
    for category, message in errors.items():
        flash(message, category)
    return len(errors) == 0




def update_user_validate(data):
    errors = {}
    if 'email'in data and not EMAIL_REGEX.match(data['email']):
        errors['email'] = 'Please enter valid Email'
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
  
