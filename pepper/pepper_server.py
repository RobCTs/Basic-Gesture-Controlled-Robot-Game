# # Unnecessary because we are cloning the repo inside this folder so we can use linting with the IDE for development

# import sys
# import os

# pdir = os.getenv('PEPPER_TOOLS_HOME')
# sys.path.append(pdir+ '/cmd_server')

# import pepper_cmd
# from pepper_cmd import *

import pepper_tools.cmd_server.pepper_cmd as pepper_cmd
from chat_management import get_robot_dialog
from flask import Flask, request
from flask_restful import Api

pepper_cmd.begin()

app = Flask(__name__)

@app.route('/get_robot_dialog', methods=['POST'])
def chat_management():
    dialog_type = request.json['dialog_type']
    params = request.json['params']
    params = dict(params)
    robot_says = get_robot_dialog(dialog_type, params)
    pepper_cmd.robot.say(robot_says)
    return "Success"






