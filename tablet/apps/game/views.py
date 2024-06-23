import datetime
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
game_text = "Make your move!"
player_score = 0
current_round = 0
playing_rps = False
over_rps = False
timer_pred_rps = datetime.datetime.now()
timer_round_rps = datetime.datetime.now()
predictions_round_rps = []

PREDS_PER_SEC = 10
ROUND_TIME = 3
TOTAL_ROUNDS = 5

def gen_frames():
    global player_move, computer_move, game_text, player_score, current_round, playing_rps, over_rps, timer_pred_rps, timer_round_rps, predictions_round_rps
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            if playing_rps:
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

                # If the round time has elapsed, determine the winner of the round
                time_elapsed_round = current_time - timer_round_rps
                if time_elapsed_round.total_seconds() >= ROUND_TIME:
                    timer_round_rps = current_time
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
                        current_round += 1
                        predictions_round_rps = []

                if current_round >= TOTAL_ROUNDS:
                    playing_rps = False
                    over_rps = True

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
    
    return render_template('game/rock_paper_scissors.html', playing_rps=playing_rps)

@game.route('/start_game')
def start_game():
    global playing_rps, over_rps
    playing_rps = True
    over_rps = False

    # Reset the game status
    global player_move, computer_move, game_text, player_score, current_round, timer_rps, predictions_round_rps, timer_round_rps
    player_move = None
    computer_move = None
    game_text = "Make your move!"
    player_score = 0
    current_round = 0
    timer_rps = datetime.datetime.now()
    timer_round_rps = datetime.datetime.now()
    predictions_round_rps = []

    # Refresh the rock paper scissors page with playing_rps set to True
    return render_template('game/rock_paper_scissors.html', playing_rps=playing_rps)

@game.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@game.route('/get_game_status')
def get_game_status():
    global player_move, computer_move, game_text, player_score, current_round, TOTAL_ROUNDS, over_rps
    return jsonify({
        'player_move': player_move,
        'computer_move': computer_move,
        'game_text': game_text,
        'player_score': player_score,
        'current_round': current_round,
        'total_rounds': TOTAL_ROUNDS,
        'over_rps': over_rps
    })

@game.route('/rock_paper_scissors_result')
def rock_paper_scissors_result():
    global playing_rps, over_rps, player_score
    playing_rps = False
    over_rps = False

    final_text = "You won!" if player_score > 0 else "You lost!" if player_score < 0 else "It's a tie!"
    return render_template('game/rock_paper_scissors_result.html', player_score=player_score, final_text=final_text)


# COPYCAT GAME


@game.route('/copycat')
def copycat():
    return '<h1>Copy Cat</h1>'
