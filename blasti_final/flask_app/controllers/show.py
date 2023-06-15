from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.categorie import Category 
from flask_app.models.business import Business
from flask_app.models.service import Services



@app.route('/show')
def show_page():
    if 'user_id' in session:
        services = Services.get_all_service()
        categories = Category.get_all_categories()
        # print("----------------cat__"+categories[0].name)
        businesses = Business.get_all()

        return render_template("show.html", categories=categories,businesses=businesses,services=services)
    return redirect('/')