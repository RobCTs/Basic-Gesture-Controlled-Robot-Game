import httpx
from bridge_pepper.utils import DialogType
import time

def get_robot_dialog(dialog_type: DialogType = DialogType.INITIAL_GREETING, params: dict = {}, delay_ms: int = 0):

    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    
    response = httpx.post('http://localhost:5000/get_robot_dialog', json={
        'dialog_type': dialog_type.value,
        'params': params
    }, timeout=10)
    return response.text