import httpx
from bridge_pepper.utils import DialogType, PostureType
import time

def get_robot_dialog(dialog_type: DialogType = DialogType.INITIAL_GREETING, params: dict = {}, delay_ms: int = 0):

    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    
    response = httpx.post('http://localhost:5000/get_robot_dialog', json={
        'dialog_type': dialog_type.value,
        'params': params
    }, timeout=10)
    return response.text

def set_posture(posture: PostureType = PostureType.NORMAL, delay_ms: int = 0, time_s = 3.0):
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    response = httpx.post('http://localhost:5000/set_posture', json={
        'time': time_s,
        'posture': posture.value
    }, timeout=10)
    return response.text

def get_asr_sentence(delay_ms: int = 0):
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    response = httpx.get('http://localhost:5000/get_asr_sentence', timeout=10)
    return response.text