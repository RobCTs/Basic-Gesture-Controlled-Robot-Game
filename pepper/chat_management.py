

def get_robot_dialog(dialog_type, params):
    robot_says = ""
    if dialog_type == "initial.greeting":
        robot_says = "Welcome Human! I am Pepper, to start, you can talk to me by saying 'Pepper' or Touch the Button on my chest."
    if dialog_type == "initial.info_name_age":
        robot_says = "Please, tell me your name and age by saying: Name: Your Name, Age: Your Age, or fill in the form on the tablet."
    if dialog_type == "initial.info_finalized":
        robot_says = "Thank you! I will remember that you are " + str(params["age"]) + " years old, " + params["name"] + "."
    if dialog_type == "game.choose_game":
        robot_says = "Tell me which game to play: Rock Paper Scissors or Copycat, or touch the button on the tablet."
    if dialog_type == "game.rock_paper_scissors.start":
        robot_says = "Let's play Rock Paper Scissors, " + params["name"] + ". You can start by saying Start or clicking the button on the tablet. You will have 3 seconds to make your move each round, and there will be 5 rounds in total. Keep your pose steady during the 3 seconds."
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
    return robot_says