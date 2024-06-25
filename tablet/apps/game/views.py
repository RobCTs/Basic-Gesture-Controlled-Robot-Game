import datetime
import json
import threading
from flask import Blueprint, Response, jsonify
from flask import render_template

game = Blueprint('game', __name__, template_folder='templates', static_folder='static')

# Importing Libraries
import time
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import numpy as np
import cv2
import random
import pickle
from bridge_pepper.bridge import get_robot_dialog, set_posture
from bridge_pepper.utils import DialogType, PostureType


# Load the TFLite model from the same folder as the script
MODEL_FOLDER = "D:\\Documents\\GitHub\\Basic-Gesture-Controlled-Robot-Game\\tablet\\apps\\game\\rockpaperscissors\\"
interpreter = tf.lite.Interpreter(model_path=MODEL_FOLDER + "model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the label encoder from pickle file
with open(MODEL_FOLDER + "labelencoder.pkl", "rb") as le_dump_file:
    label_encoder: LabelEncoder = pickle.load(le_dump_file)

# Function to preprocess the image
def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 300))  # Resize to 300x300
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize the image
    image = image.astype(np.float32)

    # Convert the image to the format expected by the TFLite model, from (1, 300, 300, 3) to (1, 3, 300, 300), keeping the order of the x and y
    image = np.transpose(image, (0, 3, 1, 2))
    return image


# Function to predict the gesture from an image using the TFLite model
def predict_single_image(interpreter, image, label_encoder):
    image = preprocess_image(image)

    # Set the tensor
    interpreter.set_tensor(input_details[0]["index"], image)
    interpreter.invoke()

    # Get the prediction
    output_data = interpreter.get_tensor(output_details[0]["index"])
    predicted_label = np.argmax(output_data)
    label = label_encoder.inverse_transform([predicted_label])[0]
    return label

# Rock Paper Scissors conversion to the dataset classes
rock = ["fist"]
paper = ["palm", "stop", "stop_inverted"]
scissors = ["peace", "peace_inverted"]

# Function to convert the prediction to rock, paper, or scissors
def convert_prediction(prediction):
    if prediction in rock:
        return "rock"
    elif prediction in paper:
        return "paper"
    elif prediction in scissors:
        return "scissors"
    else:
        return "Not Valid"
    

# Global variables to store game status
player_move = None
computer_move = None
instant_player_move = None
game_text = "Make your move!"
player_score = 0
current_round = 0
playing_rps = False
over_rps = False
inter_round_paused = False
timer_inter_round = datetime.datetime.now()
timer_pred_rps = datetime.datetime.now()
timer_round_rps = datetime.datetime.now()
predictions_round_rps = []

PREDS_PER_SEC = 10
ROUND_TIME = 4
TOTAL_ROUNDS = 5
INTER_ROUND_TIME = 5

def gen_frames():
    global player_move, computer_move, game_text, player_score, current_round, playing_rps, over_rps, timer_pred_rps, timer_round_rps, predictions_round_rps, inter_round_paused, timer_inter_round, instant_player_move
    cap = cv2.VideoCapture(0)

    age = None
    current_user = None
    # Get current user and age
    with open('session/info.json', 'r') as f:
        data = json.load(f)
        current_user = data['currentUser']
        for user in data['registeredUsers']:
            if user['name'] == current_user:
                age = user['age']
                break
    if age is None:
        age = 18

    
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            if playing_rps:
                if inter_round_paused:
                    current_time = datetime.datetime.now()
                    time_elapsed_inter_round = current_time - timer_inter_round
                    if time_elapsed_inter_round.total_seconds() >= INTER_ROUND_TIME:
                        inter_round_paused = False
                        timer_pred_rps = current_time
                        timer_round_rps = current_time
                        current_round += 1
                        predictions_round_rps = []
                        game_text = "Make your move!"

                        y = threading.Thread(target=set_posture, args=(PostureType.NORMAL, 0, 2.0, age))
                        y.start()
                else:
                    current_time = datetime.datetime.now()
                    time_elapsed_pred = current_time - timer_pred_rps

                    # For each 1/PRED_PER_SEC seconds, capture the player's move
                    if time_elapsed_pred.total_seconds() >= 1 / PREDS_PER_SEC:
                        timer_pred_rps = current_time
                        # Keep the frame dimensions intact
                        frame_height, frame_width = frame.shape[:2]
                        min_dim = min(frame_height, frame_width)
                        start_x = frame_width // 2 - min_dim // 2
                        end_x = frame_width // 2 + min_dim // 2
                        start_y = frame_height // 2 - min_dim // 2
                        end_y = frame_height // 2 + min_dim // 2
                        cropped_frame = frame[start_y:end_y, start_x:end_x]

                        prediction = predict_single_image(interpreter, cropped_frame, label_encoder)
                        predictions_round_rps.append(prediction)
                        instant_player_move = convert_prediction(prediction)
                        player_move = max(set(predictions_round_rps), key=predictions_round_rps.count)
                        player_move = convert_prediction(player_move)

                    # If the round time has elapsed, determine the winner of the round
                    time_elapsed_round = current_time - timer_round_rps
                    if time_elapsed_round.total_seconds() >= ROUND_TIME:
                        if predictions_round_rps:
                            player_move = max(set(predictions_round_rps), key=predictions_round_rps.count)
                            player_move = convert_prediction(player_move)
                            computer_move = random.choice(["rock", "paper", "scissors"])
                            if player_move == computer_move:
                                game_text = "It's a tie!"
                            elif (player_move == "rock" and computer_move == "scissors") or \
                                    (player_move == "paper" and computer_move == "rock") or \
                                    (player_move == "scissors" and computer_move == "paper"):
                                game_text = "Player Wins!"
                                player_score += 1
                            else:
                                game_text = "Computer Wins!"
                                player_score -= 1

                            inter_round_paused = True
                            timer_inter_round = current_time
                            x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_ROCK_PAPER_SCISSORS_ROUND, {'rps_move': player_move, 'rps_round_winner': 'player' if game_text == 'Player Wins!' else 'computer' if game_text == 'Computer Wins!' else 'tie'}))
                            x.start()

                            # Set Robot Posture
                            if computer_move == "rock":
                                y = threading.Thread(target=set_posture, args=(PostureType.ROCK, 0, 1.5, age))
                                y.start()
                            elif computer_move == "paper":
                                y = threading.Thread(target=set_posture, args=(PostureType.PAPER, 0, 1.5, age))
                                y.start()
                            elif computer_move == "scissors":
                                y = threading.Thread(target=set_posture, args=(PostureType.SCISSORS, 0, 1.5, age))
                                y.start()
                            

                if current_round >= TOTAL_ROUNDS:
                    playing_rps = False
                    over_rps = True
                    inter_round_paused = False

            # Encode the frame to send it as a response
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@game.route('/rock_paper_scissors')
def rock_paper_scissors():
    global playing_rps, over_rps
    playing_rps = False
    over_rps = False
    
    age = None
    current_user = None
    # Get current user and age
    with open('session/info.json', 'r') as f:
        data = json.load(f)
        current_user = data['currentUser']
        for user in data['registeredUsers']:
            if user['name'] == current_user:
                age = user['age']
                break
    if age is None:
        age = 18

    
    if not playing_rps:
        x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_ROCK_PAPER_SCISSORS_START, {'name': current_user }))
        x.start()
    
    return render_template('game/rock_paper_scissors.html', playing_rps=playing_rps)

@game.route('/start_game')
def start_game():
    global playing_rps, over_rps
    playing_rps = True
    over_rps = False

    # Reset the game status
    global player_move, computer_move, game_text, player_score, current_round, timer_rps, predictions_round_rps, timer_round_rps, inter_round_paused, timer_inter_round, instant_player_move
    player_move = None
    computer_move = None
    instant_player_move = None
    game_text = "Make your move!"
    player_score = 0
    current_round = 0
    timer_rps = datetime.datetime.now()
    timer_round_rps = datetime.datetime.now()
    inter_round_paused = False
    timer_inter_round = datetime.datetime.now()
    predictions_round_rps = []

    # Refresh the rock paper scissors page with playing_rps set to True
    return render_template('game/rock_paper_scissors.html', playing_rps=playing_rps)

@game.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@game.route('/get_game_status')
def get_game_status():
    global player_move, computer_move, game_text, player_score, current_round, TOTAL_ROUNDS, over_rps, inter_round_paused, instant_player_move
    return jsonify({
        'player_move': player_move,
        'instant_player_move': instant_player_move,
        'computer_move': computer_move,
        'game_text': game_text,
        'player_score': player_score,
        'current_round': current_round,
        'total_rounds': TOTAL_ROUNDS,
        'over_rps': over_rps,
        'inter_round_paused': inter_round_paused
    })

@game.route('/rock_paper_scissors_result')
def rock_paper_scissors_result():
    global playing_rps, over_rps, player_score
    playing_rps = False
    over_rps = False

    final_text = "You won!" if player_score > 0 else "You lost!" if player_score < 0 else "It's a tie!"

    x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_ROCK_PAPER_SCISSORS_OVER, {'player_score': player_score}))
    x.start()

    return render_template('game/rock_paper_scissors_result.html', player_score=player_score, final_text=final_text)


# Guess My Gesture Game

# Global variables to store game status
playing_gesture = False
over_gesture = False
current_round_gesture = 0
game_text_gesture = "Make your move!"
player_move_gesture = None
instant_player_move_gesture = None
inter_round_paused_gesture = False
timer_inter_round_gesture = datetime.datetime.now()
timer_gesture = datetime.datetime.now()
timer_pred_gesture = datetime.datetime.now()
predictions_round_gesture = []

PREDS_PER_SEC_GESTURE = 10
ROUND_TIME_GESTURE = 4
TOTAL_ROUNDS_GESTURE = 5
INTER_ROUND_TIME_GESTURE = 5


def format_prediction(prediction):
    return prediction.replace("_", " ").capitalize()

def gen_frames_gestures():
    global game_text_gesture, current_round_gesture, playing_gesture, over_gesture, timer_pred_gesture, timer_inter_round_gesture, predictions_round_gesture, inter_round_paused_gesture, timer_inter_round_gesture, instant_player_move_gesture, player_move_gesture
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            if playing_gesture:
                if inter_round_paused_gesture:
                    current_time = datetime.datetime.now()
                    time_elapsed_inter_round = current_time - timer_inter_round_gesture
                    if time_elapsed_inter_round.total_seconds() >= INTER_ROUND_TIME_GESTURE:
                        inter_round_paused_gesture = False
                        timer_pred_gesture = current_time
                        timer_inter_round_gesture = current_time
                        current_round_gesture += 1
                        predictions_round_gesture = []
                        game_text_gesture = "Make your move!"
                else:
                    current_time = datetime.datetime.now()
                    time_elapsed_pred = current_time - timer_pred_gesture

                    # For each 1/PRED_PER_SEC seconds, capture the player's move
                    if time_elapsed_pred.total_seconds() >= 1 / PREDS_PER_SEC_GESTURE:
                        timer_pred_gesture = current_time
                        # Keep the frame dimensions intact
                        frame_height, frame_width = frame.shape[:2]
                        min_dim = min(frame_height, frame_width)
                        start_x = frame_width // 2 - min_dim // 2
                        end_x = frame_width // 2 + min_dim // 2
                        start_y = frame_height // 2 - min_dim // 2
                        end_y = frame_height // 2 + min_dim // 2
                        cropped_frame = frame[start_y:end_y, start_x:end_x]

                        prediction = predict_single_image(interpreter, cropped_frame, label_encoder)
                        predictions_round_gesture.append(prediction)
                        instant_player_move_gesture = format_prediction(prediction)
                        player_move_gesture = max(set(predictions_round_gesture), key=predictions_round_gesture.count)
                        player_move_gesture = format_prediction(player_move_gesture)

                    # If the round time has elapsed, determine the winner of the round
                    time_elapsed_round = current_time - timer_inter_round_gesture
                    if time_elapsed_round.total_seconds() >= ROUND_TIME_GESTURE:
                        if predictions_round_gesture:
                            player_move_gesture = max(set(predictions_round_gesture), key=predictions_round_gesture.count)
                            player_move_gesture = format_prediction(player_move_gesture)

                            inter_round_paused_gesture = True
                            timer_inter_round_gesture = current_time
                            x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_GUESS_MY_GESTURE_ROUND, {'gesture_player': player_move_gesture}))
                            x.start()
                            

                if current_round_gesture >= TOTAL_ROUNDS_GESTURE:
                    playing_gesture = False
                    over_gesture = True
                    inter_round_paused_gesture = False

            # Encode the frame to send it as a response
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@game.route('/guess_my_gesture')
def guess_my_gesture():
    global playing_gesture, over_gesture
    playing_gesture = False
    over_gesture = False
    
    age = None
    current_user = None
    # Get current user and age
    with open('session/info.json', 'r') as f:
        data = json.load(f)
        current_user = data['currentUser']
        for user in data['registeredUsers']:
            if user['name'] == current_user:
                age = user['age']
                break
    if age is None:
        age = 18

    
    if not playing_gesture:
        x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_GUESS_MY_GESTURE_START, {'name': current_user }))
        x.start()
    
    return render_template('game/guess_my_gesture.html', playing_gesture=playing_gesture)


@game.route('/start_game_gesture')
def start_game_gesture():
    global playing_gesture, over_gesture
    playing_gesture = True
    over_gesture = False

    # Reset the game status
    global player_move_gesture, game_text_gesture, current_round_gesture, timer_gesture, predictions_round_gesture, timer_gesture, inter_round_paused_gesture, timer_inter_round_gesture, instant_player_move_gesture, timer_pred_gesture
    player_move_gesture = None
    game_text_gesture = "Make your move!"
    current_round_gesture = 0
    timer_gesture = datetime.datetime.now()
    timer_pred_gesture = datetime.datetime.now()
    inter_round_paused_gesture = False
    timer_inter_round_gesture = datetime.datetime.now()
    predictions_round_gesture = []

    # Refresh the rock paper scissors page with playing_gesture set to True
    return render_template('game/guess_my_gesture.html', playing_gesture=playing_gesture)

@game.route('/video_feed_gesture')
def video_feed_gesture():
    return Response(gen_frames_gestures(), mimetype='multipart/x-mixed-replace; boundary=frame')



@game.route('/get_game_status_gesture')
def get_game_status_gesture():
    global player_move_gesture, game_text_gesture, current_round_gesture, TOTAL_ROUNDS_GESTURE, over_gesture, inter_round_paused_gesture, instant_player_move_gesture
    return jsonify({
        'player_move': player_move_gesture,
        'instant_player_move': instant_player_move_gesture,
        'game_text': game_text_gesture,
        'current_round': current_round_gesture,
        'total_rounds': TOTAL_ROUNDS_GESTURE,
        'over_gesture': over_gesture,
        'inter_round_paused': inter_round_paused_gesture
    })

@game.route('/gesture_end')
def gesture_end():
    global playing_gesture, over_gesture
    playing_gesture = False
    over_gesture = False

    final_text = "The game is over!"

    x = threading.Thread(target=get_robot_dialog, args=(DialogType.GAME_GUESS_MY_GESTURE_OVER,))
    x.start()

    return render_template('game/guess_my_gesture_end.html', final_text=final_text)
