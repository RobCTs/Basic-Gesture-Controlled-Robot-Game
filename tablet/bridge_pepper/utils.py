# All possible dialog types from: pepper/chat_management.py
from enum import Enum

class DialogType(Enum):
    INITIAL_GREETING = "initial.greeting"
    INITIAL_INFO_NAME_AGE = "initial.info_name_age"
    INITIAL_INFO_FINALIZED = "initial.info_finalized"
    GAME_CHOOSE_GAME = "game.choose_game"
    GAME_ROCK_PAPER_SCISSORS_START = "game.rock_paper_scissors.start"
    GAME_ROCK_PAPER_SCISSORS_ROUND = "game.rock_paper_scissors.round"
    GAME_ROCK_PAPER_SCISSORS_OVER = "game.rock_paper_scissors.over"

class PostureType(Enum):
    NORMAL = "normal"
    PAPER = "paper"
    SCISSORS = "scissors"
    ROCK = "rock"
