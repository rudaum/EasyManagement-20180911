from flask import Blueprint, render_template

page = Blueprint('page', __name__, template_folder='templates')

@page.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@page.route('/users', methods=['GET', 'POST'])
@page.route('/users/<user>', methods=['GET', 'POST'])
def users(user=None):
    return render_template('users.html', user=user)

