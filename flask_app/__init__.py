from flask import Flask, session
from flask_bcrypt import Bcrypt
import json
import os
import stripe

app = Flask(__name__)
DB = "ecommerce"# add schema name

app.config['STRIPE_PUBLIC-KEY'] = 'pk_test_51KI2GcLLVOT4TBHeHHSEeFmQJXqxQyPnhg2PSkH4cmjCca7FtpYiFRf5wGUn9AHJeLlEhA6YrRYYLXlVyPW6fSqb005QgIrhGP'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KI2GcLLVOT4TBHe29MT6xpLZWJ6zx0J2Q5kDWzmWyjNVO8GoBbaMzsHWiQeuPvgBeMoa21FHYm8bLZrzuzZDKdz00zrQga2Yu'
bcrypt = Bcrypt(app)
app.secret_key = "supersecrect"