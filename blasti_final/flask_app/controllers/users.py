from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.business import Business
from flask_bcrypt import Bcrypt
from flask_app.models.favorites import Favorites



bcrypt = Bcrypt(app)     #               we are creating an object called bcrypt,
#                          which is made by invoking the function Bcrypt with our app as an argument
from flask_app.models.categorie import Category
@app.route('/join/user')
def index_user():
    return render_template("index.html")
@app.route('/users/create',methods=['POST'])
def create_user():
    print(request.form)
    if not (User.validate(request.form)):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
            **request.form,
            'password':pw_hash
        }
    user_id = User.create_user(data)
    session['user_id'] = user_id
    print('user_id===============',user_id)
    return redirect('/main_page')

@app.route('/main_page')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data={'id':session['user_id']}
    print('data=========',data)
    user = User.get_by_id(data)
    categories = Category.get_first_categories()
    business =  Business.get_first_4_businesses()

    return render_template("main_page.html", user = user, categories = categories , business=business)

@app.route('/users/login', methods=['POST'])
def login_user():
    user_from_db = User.get_by_email({'email':request.form['email']})
    if(user_from_db):
        #                                      check password
        if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        #                        if we get False after checking the password
            flash("Invalid Password")
            return redirect('/')
        session['user_id'] = user_from_db.id
        return redirect('/main_page')
    flash("Invalid Email")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



# @app.route('/category/page')
# def category_page():
#     if 'user_id' in session:
#         return render_template("category_page.html")
#     return redirect('/')



@app.route('/dashboard')
def My_Appointments():
    if 'user_id' in session:
        return render_template("dashboard.html",business=Business.get_all(),favorites=Favorites.get_all_favorites())
    return redirect('/')