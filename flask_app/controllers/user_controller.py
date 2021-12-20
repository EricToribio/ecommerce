from flask import render_template,request,redirect,session,flash
from flask_app.models import user_model#enter model name`
from flask_app import app, bcrypt
from flask_app.config.helper import login_required



@app.route('/register/user')
def register():
    return render_template('registration.html')

@app.route('/logout')
@login_required
def log_out():
    session.clear()
    return redirect('/')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/edit/user')
@login_required
def edit_user():
    return render_template('edit_account.html', user= user_model.User.get_one(id=session['user_id']))

@app.post('/login/user')
def login_user():
    user = user_model.User.get_one(email=request.form['email'])
    if not user:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/')

@app.post('/add/user')
def add_user():
    if not user_model.User.validate_new_user(request.form):
        return redirect('/register/user')
    user=user_model.User.add_user(request.form)
    session['user_id'] = user
    return redirect('/dashboard')

