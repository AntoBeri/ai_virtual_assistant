import subprocess
import os

# Map common app names to their executable paths
APP_MAP = {
    # Browsers
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "opera": r"C:\Users\anton\AppData\Local\Programs\Opera GX\opera.exe",
    
    # Media
    "spotify": r"C:\Users\{username}\AppData\Roaming\Spotify\Spotify.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",

    # Other apps
    "roblox": r"C:\Users\{username}\AppData\Local\Roblox\Versions\version-bf6344c9c23446bf\RobloxPlayerBeta.exe",
    
    # Development
    "vscode": r"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "terminal": "wt.exe",  # Windows Terminal, already on PATH
    
    # System
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    
    # Communication
    "discord": r"C:\Users\{username}\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "whatsapp": r"C:\Users\{username}\AppData\Local\WhatsApp\WhatsApp.exe",
}

# tries multiple common Windows username env variables:
USERNAME = (
    os.getenv("USERNAME") or 
    os.getenv("USER") or 
    os.getenv("USERPROFILE", "").split("\\")[-1]
)

APP_MAP = {k: v.replace("{username}", USERNAME) for k, v in APP_MAP.items()}

def open_app(app_name):
    app_name = app_name.lower().strip()
    
    # Direct match
    if app_name in APP_MAP:
        path = APP_MAP[app_name]
        try:
            subprocess.Popen(path)
            return f"{app_name.capitalize()} is opening, sir."
        except FileNotFoundError:
            return f"I couldn't find {app_name} at the expected path, sir. You may need to update the path in my configuration."
        except Exception as e:
            return f"Something went wrong opening {app_name}, sir. {str(e)}"
    
    # Fuzzy match — catch close names like "vs code" -> "vscode"
    for key in APP_MAP:
        if key in app_name or app_name in key:
            path = APP_MAP[key]
            try:
                subprocess.Popen(path)
                return f"{key.capitalize()} is opening, sir."
            except FileNotFoundError:
                return f"I found a match for {key} but couldn't locate the executable, sir."
    
    return f"I don't have {app_name} in my app list, sir. You can add it to my configuration."