from functools import wraps
from flask import flash, session, redirect

def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/')
        return view(*args, **kwargs)
    return inner


# def logged_in(func):
#     @wraps(func)
#     def inner(*args,**kwargs)