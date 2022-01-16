from flask import render_template,request,jsonify,session,redirect
from flask_app.config.helper import login_required
from flask_app import app
from flask_app.models import user_model,shopping_cart_products,products


@app.route('/show/cart/<int:id>')
@login_required
def shopping_cart(id):
    user = user_model.User.get_one_join(shopping_cart_id=id)
    cart =products.Product.get_products_cart(shopping_cart_id=id)
    total = 0
    product_count = 0
    for item in cart:
        product_count += 1
        total += item.price
    
    return render_template(
        'shopping_cart.html',
        cart=cart,
        user=user,
        total=total,
        product_count=product_count,
        
        )

@app.post('/add/to/cart/<int:id>')
@login_required
def add_to_cart(id):
    shopping_cart_products.Shopping_cart_product.add_to_cart(request.form)
    return redirect(f'/show/cart/{id}')


@app.route('/delete/cart/item/<int:id>')
@login_required
def delete_item_from_cart(id):
    user = user_model.User.get_one_join(id=session['user_id'])
    data ={
        'product_id' : id,
        'shopping_cart_id': user.shopping_cart_id

    }
    delete_cart_item = shopping_cart_products.Shopping_cart_product.delete_item(data)
    return redirect(f'/show/cart/{user.shopping_cart_id}')