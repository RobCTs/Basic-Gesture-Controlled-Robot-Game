

import time

asr_sentence = ""
asr_listening = False

def get_robot_dialog(dialog_type, params):
    robot_says = ""
    listen_answer = False
    answer_choices = None
    if dialog_type == "initial.greeting":
        robot_says = "Welcome Human! I am Pepper, to start, you can talk to me by saying 'Pepper' or Touch the Button on my chest."
        listen_answer = True
        answer_choices = ["Pepper"]
    if dialog_type == "initial.info_name_age":
        robot_says = "Please, tell me your name and age by saying: Name: Your Name, Age: Your Age, or fill in the form on the tablet."
        listen_answer = True
    if dialog_type == "initial.info_finalized":
        robot_says = "Thank you! I will remember that you are " + str(params["age"]) + " years old, " + params["name"] + "."
    if dialog_type == "game.choose_game":
        robot_says = "Tell me which game to play: Rock Paper Scissors or Guess My Gesture, or touch the button on the tablet."
        listen_answer = True
        answer_choices = ["Rock Paper Scissors", "Guess My Gesture"]
    if dialog_type == "game.rock_paper_scissors.start":
        robot_says = "Let's play Rock Paper Scissors, " + params["name"] + ". You can start by saying Start or clicking the button on the tablet. You can go back saying Go Back. You will have 3 seconds to make your move each round, and there will be 5 rounds in total. Keep your pose steady during the 3 seconds."
        listen_answer = True
        answer_choices = ["Start", "Go Back"]
    if dialog_type == "game.rock_paper_scissors.round":
        robot_says = str(params["rps_move"]) + "!"
        if params["rps_round_winner"] == "player":
            robot_says += " You win this round!"
        elif params["rps_round_winner"] == "computer":
            robot_says += " I win this round!"
        else:
            robot_says += " It's a tie!"
    if dialog_type == "game.rock_paper_scissors.over":
        robot_says = "Game Over! Your score is " + str(params["player_score"]) + "."
        if params["player_score"] > 0:
            robot_says += " You win!"
        elif params["player_score"] < 0:
            robot_says += " I win!"
        else:
            robot_says += " It's a tie!"
        robot_says += " Say 'Play Again' to play again or 'Choose Game' to choose another game."
        listen_answer = True
        answer_choices = ["Play Again", "Choose Game"]
    if dialog_type == "game.guess_my_gesture.start":
        robot_says = "Let's play Guess My Gesture, " + params["name"] + ". You can start by saying Start or clicking the button on the tablet. You can go back saying Go Back. You will have 3 seconds to make your move each round, and there will be 5 rounds in total. Keep your pose steady during the 3 seconds."
        listen_answer = True
        answer_choices = ["Start", "Go Back"]
    if dialog_type == "game.guess_my_gesture.round":
        robot_says = "You made a " + str(params["gesture_player"]) + " gesture!"
    if dialog_type == "game.guess_my_gesture.over":
        robot_says = "Game Over! Say 'Play Again' to play again or 'Choose Game' to choose another game."
        listen_answer = True
        answer_choices = ["Play Again", "Choose Game"]
    return robot_says, listen_answer, answer_choices

def reset_asr(robot):
    robot.memory_service.insertData(robot.fakeASRkey, '')


def stop_asr_listening():
    global asr_listening
    asr_listening = False
    print("ASR Listening Stopped")

def get_asr_listening():
    global asr_listening
    return asr_listening

def get_asr_sentence():
    global asr_sentence
    return asr_sentence

def get_asr_sentence_and_reset_if_sent():
    global asr_sentence, asr_listening
    sentence = asr_sentence
    if sentence != "":
        asr_sentence = ""
        stop_asr_listening()
    return sentence

def asr(robot, timeout=3, dt=0.2, choices=None):
    global asr_sentence, asr_listening
    asr_listening = True


    reset_asr(robot)
    asr_sentence = ''
    log_message = "Listening for ASR"
    if choices:
        log_message += " with choices: " + ", ".join(choices)
    print(log_message)
    rolling_timeout = timeout
    while rolling_timeout > 0 and asr_listening:
        time.sleep(dt)
        rolling_timeout -= dt
        asr_sentence = robot.memory_service.getData(robot.fakeASRkey)
        if asr_sentence:
            if choices:
                if asr_sentence in choices:
                    break
                else:
                    asr_sentence = ''
                    reset_asr(robot)
                    robot.say("Not a valid choice. You can say the following: " + ", ".join(choices) + ". Try again.")
            else:
                break

    if asr_sentence == '' and asr_listening:
        stop_asr_listening()
        return "N/A"
    else:
        print("ASR Detected: " + asr_sentence)
        stop_asr_listening()
        return asr_sentence

