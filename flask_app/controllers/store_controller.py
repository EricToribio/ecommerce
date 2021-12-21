from flask import render_template,request,redirect,session
from flask_app.models import user_model, categories, products#enter model name`
from flask_app import app
from flask_app.config.helper import login_required
import os

@app.route("/")
@app.route("/dashboard")
def dashboard():
    
    all_categories = categories.Category.get_all()
    if 'user_id' in session:
        user = user_model.User.get_one_join(id=session['user_id'])
        return render_template('dashboard.html',user =user,all_categories=all_categories)
    return render_template('dashboard.html',all_categories=all_categories)

@app.route('/edit/product')
@login_required
def edit_product():
    user= user_model.User.get_one_join(id=session['user_id'])
    one_product = products.Product.get_one(id=4)
    return render_template('edit_product.html' ,one_product=one_product,user=user)

@app.route('/new/product')
@login_required
def add_product():
    user= user_model.User.get_one_join(id=session['user_id'])
    category = categories.Category.get_all()
    return render_template('add_product.html', user= user, category = category)

@app.post('/add/new/product')
def and_new_product():
    picture = request.files.get('picture')
    if picture:
        picture.save(os.path.join(app.static_folder, f"img/{session['user_id']}_{request.form['name']}.webp"))
    products.Product.add_product(request.form)
    return redirect('/dashboard')