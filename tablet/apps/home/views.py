import os
from flask import Blueprint, redirect, url_for
from flask import render_template
import json

from apps.home.forms import InfoForm

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def index():
    return render_template('home/home.html')

@home.route('/getinfo', methods=["GET", "POST"])
def getinfo():
    form = InfoForm()

    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data

        if not os.path.exists('session'):
            os.makedirs('session')

        if not os.path.exists('session/info.json'):
            data = {'currentUser': '', 'registeredUsers': []}
        else:
            with open('session/info.json', 'r') as f:
                data = json.load(f)

        data['currentUser'] = name

        if 'registeredUsers' not in data:
            data['registeredUsers'] = []

        # Check if the user is already registered
        user_exists = False
        for user in data['registeredUsers']:
            if user['name'] == name:
                user_exists = True
                break

        if not user_exists:
            data['registeredUsers'].append({
                'name': name,
                'age': age
            })

        with open('session/info.json', 'w') as f:
            json.dump(data, f)

        return redirect(url_for('home.choose_game'))

    return render_template('home/getinfo.html', form=form)


        
@home.route('/choose_game')
def choose_game():
    # Get current user and age
    with open('session/info.json', 'r') as f:
        data = json.load(f)
        user = data['currentUser']
        age = None
        for user in data['registeredUsers']:
            if user['name'] == user:
                age = user['age']
                break
            
    return render_template('home/choose_game.html', user=user, age=age)


