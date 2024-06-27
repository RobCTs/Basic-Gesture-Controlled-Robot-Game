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

# Start the robot and get the robot object from pepper_cmd (begin() function was modified to return the robot object)
robot = pepper_cmd.begin()

# Create the Flask app responsible for the robot server endpoints
app = Flask(__name__)

# API Endpoints
@app.route('/get_robot_dialog', methods=['POST'])
def chat_management(): # This function is responsible for getting the robot dialog and listening for the answer using Fake ASR
    # Get the dialog type and parameters from the request
    dialog_type = request.json['dialog_type']
    params = request.json['params']
    params = dict(params)
    # Get the robot dialog and listen_answer flag
    robot_says, listen_answer, answer_choices = get_robot_dialog(dialog_type, params)
    # Make the robot say the dialog
    robot.say(robot_says)
    # If the dialog is a question, listen for the answer
    if listen_answer:
        # On a new thread, listen for the answer
        x = threading.Thread(target=asr, args=(robot,25,0.2,answer_choices))
        x.start()        
    return "Success"

@app.route('/stop_asr_listening', methods=['GET'])
def stop_asr(): # Route that stops the ASR listening
    stop_asr_listening()
    return "Success"

@app.route('/get_asr_sentence', methods=['GET'])
def get_asr(): # Route that gets the ASR sentence if it was already listened and resets
    sentence = get_asr_sentence_and_reset_if_sent()
    if sentence == "":
        return "N/A"
    else:
        return sentence

@app.route('/set_posture', methods=['POST'])
def set_posture(): # Route that sets the robot posture
    # Get the posture, time to execute and age from the request
    time = request.json['time']
    posture = request.json['posture']
    age = request.json['age']
    print("Setting posture: " + posture + " with time: " + str(time) + " and age: " + str(age))
    if posture == "normal":
        # Personalize the posture based on the age
        if int(age) > 12:
            normalPosture(robot, time)
        else:
            setPosture(robot, KID_NORMAL_DICT, time)
    elif posture == "paper":
        # Personalize the posture based on the age
        if int(age) > 12:
            setPosture(robot, PAPER_DICT, time)
        else:
            setPosture(robot, KID_PAPER_DICT, time)
    elif posture == "scissors":
        # Personalize the posture based on the age
        if int(age) > 12:
            setPosture(robot, SCISSORS_DICT, time)
        else:
            setPosture(robot, KID_SCISSORS_DICT, time)
    elif posture == "rock":
        # Personalize the posture based on the age
        if int(age) > 12:
            setPosture(robot, ROCK_DICT, time)
        else:
            setPosture(robot, KID_ROCK_DICT, time)
        
    return "Success"




