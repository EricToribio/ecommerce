from flask_app import app,session
from flask import render_template,redirect
from flask_app.config.helper import login_required
from flask_app.models import user_model,orders

@app.route('/past/orders')
@login_required
def place_order():
    user = user_model.User.get_one(id=session['user_id'])
    user_orders = orders.Orders.get_orders(user_order_id= session['user_id'])
    return render_template('past_orders.html', user=user,user_orders=user_orders)
