from flask_app import app

from flask_app.controllers import user_controller,product_controller,payment_controller,shopping_cart_controller #controller file name

if __name__ == "__main__":
    app.run(debug=True)