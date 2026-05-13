import subprocess
import os
from config import config

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