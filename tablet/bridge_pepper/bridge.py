import httpx
from bridge_pepper.utils import DialogType, PostureType
import time

# Function to get the robot dialog from the pepper robot server
def get_robot_dialog(dialog_type: DialogType = DialogType.INITIAL_GREETING, params: dict = {}, delay_ms: int = 0):
    # If there is a delay, wait for the specified time
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    
    # Send a POST request to the Pepper robot server to get the robot dialog
    response = httpx.post('http://localhost:5000/get_robot_dialog', json={
        'dialog_type': dialog_type.value,
        'params': params
    }, timeout=10)
    return response.text

# Function to set the posture of the robot
def set_posture(posture: PostureType = PostureType.NORMAL, delay_ms: int = 0, time_s = 3.0, age = 18):
    # If there is a delay, wait for the specified time
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    # Send a POST request to the Pepper robot server to set the posture of the robot
    response = httpx.post('http://localhost:5000/set_posture', json={
        'time': time_s,
        'posture': posture.value,
        'age': age
    }, timeout=10)
    return response.text

# Function to get the ASR sentence from the Pepper robot server
def get_asr_sentence(delay_ms: int = 0):
    # If there is a delay, wait for the specified time
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    # Send a GET request to the Pepper robot server to get the ASR sentence
    response = httpx.get('http://localhost:5000/get_asr_sentence', timeout=10)
    return response.text