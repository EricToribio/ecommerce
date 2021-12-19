from flask import render_template,request,redirect,session
from flask_app.models import user_model#enter model name`
from flask_app import app
from flask_app.config.helper import login_required


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register/user')
def register():
    return render_template('registration.html')

@app.route('/edit/user')
@login_required
def edit_user():
    return render_template('edit_account.item')

@app.post('/add/user')
def add_user():
    if not user_model.User.validate_new_user(request.form):
        return redirect('/register/user')
    
        
    user=user_model.User.add_user(request.form)
    session['user.id'] = user
    return redirect('/dashboard')