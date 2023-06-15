from flask_app import app, IMAGES_PATH
from flask import render_template, request, redirect, session, flash
from flask_app.models.business import Business
from flask_app.models.adresse import Adresse
from flask_app.models.disponibility import Disponibility
from flask_app.models.image import Image
from flask_app.models.service import Services
from flask_bcrypt import Bcrypt
from flask_app.models.categorie import Category
from flask_app.models.user import User

bcrypt = Bcrypt(app)
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='flask_app/static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#====================================== creation besiness/adresse ===========================================
#REGISTER
#render route to display the register form
@app.route('/join/business')
def index():
    return render_template("business_form.html",categorie=Category.get_all_categories())

#action route to rgestration
@app.route('/register/business' , methods=['POST'])
def register_business():
    #1 validate inputs
    if not Business.validate_business(request.form) and not Adresse.validate_adresses(request.form):
        return redirect('/')
    #2 encrypt password 
    hashed_password = Business.encrypt_string(request.form['password'])
    
    #3 send hached password instead of text passowrd
    data = {
        **request.form,
        'password':hashed_password
    }
    businesses_id = Business.create_business(data)
    if businesses_id:  # Check if the business_id is not None or empty
        Adresse.create_adresse({**data, 'businesses_id': businesses_id})
        session['business_id'] = businesses_id
        return redirect('/finish_your_besiness_creation')
    else:
        flash("Failed to create business. Please try again.")
        return redirect('/')

#=============================== set up besiness (time-service-image) ========================================

@app.route('/finish_your_besiness_creation')
def finish_your_besiness_creation():
    return render_template("set_up_business.html")

@app.route('/setup/time_images', methods=['POST'])
def setup_time_images():
    # selected_days = request.form.getlist('day')
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    service_names = request.form.getlist('service_name')
    # images = request.files.getlist('images')
    business_id = session['business_id']
    services_data = []
    image_data = []
    # Prepare data for disponibility table
 
    for key, val in request.form.items():
        for day in days:
            if key == day+"-start_time":
                Disponibility.create_disponibility(
                    {
                    'businesses_id': business_id,
                    'day': day,
                    'start_time': request.form[day+'-start_time'],
                    'end_time': request.form[day+'-end_time']}
                )
                
        
    # Prepare data for services table
    for i in range(len(service_names)):
        services_data.append({
            'service_name': service_names[i],
            'businesses_id': business_id,
        })
    
    # Prepare data for image table
    # ? =============================
    file = request.files['images']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        flash('Image successfully uploaded and displayed below')
        print("*****************",  request.files['images'])
    # return redirect('/login')
    # for i in range(len(images)):
    #     if images and allowed_file(images.filename):
    #         filename = secure_filename(images.filename)
    #         images.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    #     flash('Image successfully uploaded and displayed below')
    #     image_data.append({
    #         'images': images[i],
    #         'business_id': business_id
    #     })
    # Insert data into respective tables
    for data in services_data:
        Services.create_services(data)
        print("========", data)
    
    
    data={
        'images':request.files['images'].filename,
        'business_id':business_id
        }
    print("*****************", services_data)
    Image.create_img(data)
    return redirect('/business/profile')


# @app.route('/business/profile')
# def display_profile_info():
#     # if 'business_id' in session:
#         # business=Business.get_all_businesses({'business_id'})
#         # business=Business.get_all_businesses({'business_id': session['business']})
#     business_id = session.get(business_id)
#     business = Business.get_besiness_by_id(business_id)
#     adresses = Adresse.get_adresse_by_id(business_id)
#     disponibility = Disponibility.get_all_disponibility(business_id)
#     services = Services.get_services_by_business_id(business_id)
#     images = Image.get_images_by_business_id(business_id)
#     return render_template("business_profile.html", business_id= business_id  ,business=business, adresses=adresses, disponibility=disponibility, services=services, images=images)


@app.route('/business/profile')
def display_profile_info():
    business_id = session.get('business_id')
    if business_id:
        business = Business.get_besiness_by_id(business_id)
        addresses = Adresse.get_adresse_by_id(business_id)
        availability = Disponibility.get_disponibility_by_id(business_id)
        services = Services.get_services_by_business_id(business_id)
        images = Image.get_images_by_business_id(business_id)
        return render_template("business_profile.html", business_id=business_id, business=business, addresses=addresses, availability=availability, services=services, images=images)
    else:
        # Handle the case when 'business_id' is not in the session
        return "Business ID not found in session."


#============================================LOGIN====================
@app.route('/besiness/login', methods=['POST'])
def login():
    besiness_from_db = Business.get_by_email({'email':request.form['email']})
    if(besiness_from_db):
        if not bcrypt.check_password_hash(besiness_from_db.password, request.form['password']):
            flash("Invalid Password","log")
            return redirect('/')
        session['besiness_id'] = besiness_from_db.id
        return redirect('/business/profile')
    flash("Invalid Email","log")
    return redirect('/')




#==================================== new controller for business===============================

@app.route('/businesses/<business_id>/destroy')
def delete_business(business_id ):
    if 'user_id' in session:
        Business.delete({'id':business_id})

    return redirect('/main_page')



# ===================show page=============================
@app.route('/show/page')
def show_business_page():
    if 'user_id' in session:
        businesses = Business.get_all_businesses()
        # print("----------------cat_________"+categories[0].name)
        businesses = Business.get_all()
        return render_template("show.html",businesses=businesses)
    return redirect('/')