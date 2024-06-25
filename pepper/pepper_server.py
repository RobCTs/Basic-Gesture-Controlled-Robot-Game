# # Unnecessary because we are cloning the repo inside this folder so we can use linting with the IDE for development

# import sys
# import os

# pdir = os.getenv('PEPPER_TOOLS_HOME')
# sys.path.append(pdir+ '/cmd_server')

# import pepper_cmd
# from pepper_cmd import *

import threading
import pepper_tools.cmd_server.pepper_cmd as pepper_cmd
from chat_management import get_robot_dialog, asr, stop_asr_listening, get_asr_sentence, get_asr_sentence_and_reset_if_sent
from posture_management import setPosture, PAPER_DICT, SCISSORS_DICT, ROCK_DICT, normalPosture, KID_NORMAL_DICT, KID_PAPER_DICT, KID_SCISSORS_DICT, KID_ROCK_DICT
from flask import Flask, request
from flask_restful import Api

robot = pepper_cmd.begin()

app = Flask(__name__)

@app.route('/get_robot_dialog', methods=['POST'])
def chat_management():
    dialog_type = request.json['dialog_type']
    params = request.json['params']
    params = dict(params)
    robot_says, listen_answer, answer_choices = get_robot_dialog(dialog_type, params)
    robot.say(robot_says)
    if listen_answer:
        # On a new thread, listen for the answer
        x = threading.Thread(target=asr, args=(robot,25,0.2,answer_choices))
        x.start()        
    return "Success"

@app.route('/stop_asr_listening', methods=['GET'])
def stop_asr():
    stop_asr_listening()
    return "Success"

@app.route('/get_asr_sentence', methods=['GET'])
def get_asr():
    sentence = get_asr_sentence_and_reset_if_sent()
    if sentence == "":
        return "N/A"
    else:
        return sentence

@app.route('/set_posture', methods=['POST'])
def set_posture():
    time = request.json['time']
    posture = request.json['posture']
    age = request.json['age']
    print("Setting posture: " + posture + " with time: " + str(time) + " and age: " + str(age))
    if posture == "normal":
        if int(age) > 12:
            normalPosture(robot, time)
        else:
            setPosture(robot, KID_NORMAL_DICT, time)
    elif posture == "paper":
        if int(age) > 12:
            setPosture(robot, PAPER_DICT, time)
        else:
            setPosture(robot, KID_PAPER_DICT, time)
    elif posture == "scissors":
        if int(age) > 12:
            setPosture(robot, SCISSORS_DICT, time)
        else:
            setPosture(robot, KID_SCISSORS_DICT, time)
    elif posture == "rock":
        if int(age) > 12:
            setPosture(robot, ROCK_DICT, time)
        else:
            setPosture(robot, KID_ROCK_DICT, time)
        
    return "Success"




