from flask import render_template,request,jsonify,session
from flask_app.config.helper import login_required
from flask_app import app
from flask_app.models import user_model


@app.route('/checkout')
@login_required
def checkout():
    return render_template("checkout.html", user = user_model.User.get_one_join(id=session['user_id']))



def calculate_order_amount(items):
    
    return 1400


@app.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment():
    user = user_model.User.get_one_join(id=session['user_id'])
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': session['total_price'],
            'quantity': session['product_count'],
        }],
        mode='payment',
        success_url=url_for('/place/order', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for(f'/show/cart/{user.shopping_cart_id}', _external=True),
    )
    
    return render_template(
        'index.html', 
        checkout_session_id=session['id'], 
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )