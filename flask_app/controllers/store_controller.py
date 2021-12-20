from flask import render_template,request,redirect,session
from flask_app.models import user_model#enter model name`
from flask_app import app
from flask_app.config.helper import login_required

@app.route("/")
@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        user = user_model.User.get_one(id=session['user_id'])
        return render_template('dashboard.html',user =user)
    return render_template('dashboard.html')