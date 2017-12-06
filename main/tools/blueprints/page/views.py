from flask import Blueprint, render_template

page = Blueprint('page', __name__, template_folder='templates')

@page.route('/')
def home():
    return render_template('index.html')

@page.route('/users')
def users():
    return render_template('users.html')


