import subprocess
import os
from config import config
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

APP_MAP = config["apps"]

def open_app(app_name):
    app_name = app_name.lower().strip()
    
    # Direct match
    if app_name in APP_MAP:
        path = APP_MAP[app_name]
        try:
            subprocess.Popen(path)
            return f"{app_name.capitalize()} is opening."
        except FileNotFoundError:
            return f"I couldn't find {app_name} at the expected path. You may need to update the config file."
        except Exception as e:
            return f"Something went wrong opening {app_name}. {str(e)}"
    
    # Fuzzy match
    for key in APP_MAP:
        if key in app_name or app_name in key:
            path = APP_MAP[key]
            try:
                subprocess.Popen(path)
                return f"{key.capitalize()} is opening."
            except FileNotFoundError:
                return f"I found a match for {key} but couldn't locate the executable."
    
    return f"I don't have {app_name} in my app list. You can add it to the config file."

# volume control

def _get_volume_controller():
    """Safely retrieves the volume controller across different Pycaw versions."""
    devices = AudioUtilities.GetSpeakers()
    
    # If it's a modern AudioDevice object, access EndpointVolume directly
    if hasattr(devices, 'EndpointVolume'):
        return devices.EndpointVolume
        
    # Fallback: If it's a legacy COM pointer object, manually activate it
    if hasattr(devices, 'Activate'):
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return interface.QueryInterface(IAudioEndpointVolume)
        
    raise AttributeError("Could not resolve volume interface from audio device.")

def set_volume(level: int):
    try:
        volume = _get_volume_controller()
        level = max(0, min(100, level))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume set to {level} percent, sir."
    except Exception as e:
        return f"I couldn't adjust the volume. {str(e)}"

def get_volume():
    try:
        volume = _get_volume_controller()
        level = round(volume.GetMasterVolumeLevelScalar() * 100)
        return f"Volume is currently at {level} percent, sir."
    except Exception as e:
        return f"I couldn't read the volume level. {str(e)}"

def mute_volume():
    try:
        volume = _get_volume_controller()
        volume.SetMute(1, None)
        return "Audio muted, sir."
    except Exception as e:
        return f"I couldn't mute the audio. {str(e)}"

def unmute_volume():
    try:
        volume = _get_volume_controller()
        volume.SetMute(0, None)
        return "Audio unmuted, sir."
    except Exception as e:
        return f"I couldn't unmute the audio. {str(e)}"
    
# brightness control

def set_brightness(level: int):
    """Set brightness to a percentage 0-100"""
    try:
        level = max(0, min(100, level))
        sbc.set_brightness(level)
        return f"Brightness set to {level} percent, sir."
    except Exception as e:
        return f"I couldn't adjust the brightness. {str(e)}"

def get_brightness():
    """Get current brightness level"""
    try:
        level = sbc.get_brightness()[0]
        return f"Brightness is currently at {level} percent, sir."
    except Exception as e:
        return f"I couldn't read the brightness level. {str(e)}"