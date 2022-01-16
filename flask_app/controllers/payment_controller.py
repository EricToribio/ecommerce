from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.config.helper import login_required
from flask_app.models import user_model
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
    return redirect('/success')

@app.route('/success')
@login_required
def place_order():
    user = user_model.User.get_one(id=session['user_id'])
    return render_template('past_orders.html', user=user)

@app.route('/payment',methods=['POST'])
def payment():
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
    customer=customer.id,
    description='T-shirt',
    amount=500,
    currency='usd',
    )
    return redirect(url_for('place_order'))