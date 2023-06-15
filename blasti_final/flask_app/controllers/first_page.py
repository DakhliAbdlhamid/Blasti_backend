from flask_app import app
from flask import render_template


@app.route('/')
def indexx1():
    return render_template("first_page.html")