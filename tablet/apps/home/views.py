import os
from flask import Blueprint, redirect, url_for
from flask import render_template
import json
from bridge_pepper.bridge import get_robot_dialog, set_posture
from bridge_pepper.utils import DialogType, PostureType

from apps.home.forms import InfoForm
import threading

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/')
def index():
    x = threading.Thread(target=get_robot_dialog, args=(DialogType.INITIAL_GREETING, {}))
    x.start()

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

        x = threading.Thread(target=get_robot_dialog, args=(DialogType.INITIAL_INFO_FINALIZED, {'name': name, 'age': age}))
        x.start()

        return redirect(url_for('home.choose_game'))
    else:
        x = threading.Thread(target=get_robot_dialog, args=(DialogType.INITIAL_INFO_NAME_AGE, {}))
        x.start()

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

    x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_CHOOSE_GAME, {}, 2000))
    x.start()

    y = threading.Thread(target=set_posture, args=(PostureType.NORMAL, 0, 3.0))
    y.start()

    return render_template('home/choose_game.html', user=user, age=age)


