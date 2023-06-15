from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.categorie import Category
from flask_app.models.myappointement import Appointment
from flask_app.models.disponibility import Disponibility
from flask_app.models.service import Services

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     #               we are creating an object called bcrypt,
#                          which is made by invoking the function Bcrypt with our app as an argument



@app.route('/appointments/new/<business_id>')
def new_appointment(business_id):
    if 'user_id' in session:
        business=Disponibility.get_all_disponibility({'user_id': session['user']})
        return render_template("make_appointment.html",dispo=Disponibility.get_all_disponibility(business_id),service=Services.get_all_service())
    return redirect('/')
###ACTION ROUTE#####

@app.route('/Make/appointment',methods=['POST'])
def create__appointments():
    data = {
            **request.form,'user_id':session['user_id']
        }
    Appointment.add(data)
        
    return redirect('/appointments/new')

@app.route('/appointments/<appointment_id>/destroy')
def delete_appointment(appointment_id):
    if 'user_id' in session:
        Appointment.delete({'id':appointment_id})
    return redirect('/dashboard')

@app.route('/appointments/<id>/edit')
def edit_appointment(id):
    if 'user_id' in session:
        one_appointment=Appointment.get_by_id({'id':id})
        return render_template("make_appointment.html", appointment=one_appointment)
    return redirect('/')

##################################### ACTION ROUTE #########################################

@app.route('/Make/appointment/update' ,methods=['POST'])
def update_appointment(id):
    if(Appointment.validate(request.form)):
        Appointment.edit(request.form)
        return redirect('/appointments')
    return redirect('/appointments/'+str(id)+'/edit')