from flask import render_template,request,redirect,session,url_for ,current_app
from flask_app.models import user_model, categories, products,shopping_cart_products#enter model name`
from flask_app import app 
from flask_app.config.helper import login_required,admin_required
import os
import stripe


stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route("/")
@app.route("/dashboard")
def dashboard():
    all_categories = categories.Category.get_all()
    if 'user_id' in session:
        user = user_model.User.get_one_join(id=session['user_id'])
        return render_template('dashboard.html',user =user,all_categories=all_categories)
    return render_template('dashboard.html',all_categories=all_categories)

@app.route('/edit/product/<int:id>')
@login_required
@admin_required
def edit_product(id):
    one_product = products.Product.get_one(id=id)
    user= user_model.User.get_one_join(id=session['user_id'])
    category = categories.Category.get_all()
    if one_product.user_id != session['user_id']:
        return redirect('/dashboard')
    return render_template('edit_product.html' ,one_product=one_product,user=user, category=category)

@app.post('/product/edit/<int:id>')
@login_required
@admin_required
def proccess_edit(id):
    picture = request.files.get('picture')
    if picture:
        picture.save(os.path.join(app.static_folder, f"img/{session['user_id']}_{request.form['name']}.webp"))
    cat ={
            'name' : request.form['category_id'].lower()
        }
    check = categories.Category.get_one(name=request.form['category_id'].lower())
    if not check:
            categories.Category.add_category(cat)
    category =categories.Category.get_one(name=request.form['category_id'].lower())
    one_product = products.Product.get_one(id=id)
    data = {
        **request.form,
        "price" : int(request.form['price']),
        'quantity' : int(request.form['quantity']),
        'picture':f"{session['user_id']}_{request.form['name']}" if picture else f"{one_product.picture}",
        'category_id': category.id,
        'user_id' : session['user_id']
    }
    
    products.Product.edit_product(data, id=id)
    return redirect(f'/show/{id}')

@app.route('/show/<int:id>')
@login_required
def show_one_product(id):
    pro = products.Product.get_one(id=id)
    user = user_model.User.get_one_join(id=session['user_id'])
    return render_template('show_one_product.html', pro=pro, user=user)



@app.route('/show/category/<int:id>')
@login_required
def show_all_in_category(id):
    category = categories.Category.get_one(id=id)
    user = user_model.User.get_one(id=session['user_id'])
    return render_template('category.html', category=category,user=user)

@app.route('/new/product')
@login_required
@admin_required
def add_product():
    user= user_model.User.get_one_join(id=session['user_id'])
    category = categories.Category.get_all()
    return render_template('add_product.html', user= user, category = category)

@app.post('/add/new/product')
@login_required
@admin_required
def and_new_product():
    picture = request.files.get('picture')
    if picture:
        picture.save(os.path.join(app.static_folder, f"img/{session['user_id']}_{request.form['name']}.webp"))
    products.Product.add_product(request.form)
    return redirect('/dashboard')

@app.route('/delete/product/<int:id>')
@login_required
@admin_required
def delete_product(id):
    products.Product.delete_product(id=id)
    return redirect('/dashboard')