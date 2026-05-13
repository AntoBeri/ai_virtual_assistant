import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    
    # Resolve {username} in app paths
    username = os.path.expanduser("~").split("\\")[-1]
    config["apps"] = {
        k: v.replace("{username}", username)
        for k, v in config["apps"].items()
    }
    
    return config

# Load once at module level so everything imports from here
config = load_config()