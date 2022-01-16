from flask_app import app,session
from flask import render_template,redirect,request
from flask_app.config.helper import login_required
from flask_app.models import user_model,orders,shopping_cart_products,order_products,products
import stripe


@app.post('/pay')
@login_required
def pay():
    
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
    customer=customer.id,
    description=request.form['description'],
    amount=request.form['amount'],
    currency='usd',
    )
    order_data ={
        'user_order_id' : session['user_id'],
        'total': request.form['amount']
    }
    new_order = orders.Orders.add_order(order_data)
    user = user_model.User.get_one(id=session['user_id'])
    cart =products.Product.get_products_cart(shopping_cart_id=user.shopping_cart_id)
    for item in cart :
        data = {
            "order_id" : new_order,
            "purchased_product_id" : item.id,
            "purchased_product_name" : item.name,
            "purchased_product_description" : item.description,
            "price" : item.price
        }
        order_item = order_products.Orders_products.add_item_to_order(data)
        delete_data = {
            'product_id' : item.id,
            'shopping_cart_id': user.shopping_cart_id
        }
        shopping_cart_products.Shopping_cart_product.delete_item(delete_data)


    return redirect('/past/orders')



