import os
from flask import Blueprint, redirect, url_for
from flask import render_template
import json
from bridge_pepper.bridge import get_asr_sentence

robot = Blueprint('robot', __name__, template_folder='templates', static_folder='static')


@robot.route('/get_asr_sentence', methods=['GET'])
def get_asr(): # Get the ASR sentence Route
    sentence = get_asr_sentence()
    if sentence == "" or sentence == "N/A":
        return "N/A"
    else:
        return sentence
    