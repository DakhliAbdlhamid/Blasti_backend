from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.categorie import Category 
from flask_app.models.business import Business

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     #               we are creating an object called bcrypt,
#                          which is made by invoking the function Bcrypt with our app as an argument

@app.route('/category/page')
def category_page():
    if 'user_id' in session:
        categories = Category.get_all_categories()
        # print("----------------cat_________"+categories[0].name)
        businesses = Business.get_all()
        return render_template("category_page.html", categories=categories,businesses=businesses)
    return redirect('/')
@app.route('/category/<int:categorie_id>')
def category_by_id(categorie_id):
    if 'user_id' in session:
        category = Category.get_category_by_id({'id':categorie_id})
        business = Business.get_business_with_category_by_id({'id': categorie_id})
        print(business,'rrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        return render_template("one_category.html", cats=category, business=business)
    return redirect('/')

