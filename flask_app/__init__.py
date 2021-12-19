from flask import Flask, session
from flask_bcrypt import Bcrypt


app = Flask(__name__)
DB = "ecommerce"# add schema name
bcrypt = Bcrypt(app)
app.secret_key = "supersecrect"