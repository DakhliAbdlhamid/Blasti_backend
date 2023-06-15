from flask import Flask
from flask_app import app
from flask_app.controllers import show
from flask_app.controllers import business_controller
from flask_app.controllers import users , myaapointements,first_page,categories





if __name__ == '__main__':
    app.run(debug=True)
