import tempfile
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import ollama
import edge_tts
import asyncio
import pygame
import io
import re
import unicodedata
import speech_recognition as sr
from faster_whisper import WhisperModel
from tools import open_app
from config import config

# Pull metadata from config
MODEL = config["assistant"]["model"]
VOICE = config["assistant"]["voice"]
WHISPER_MODEL = config["assistant"]["whisper_model"]
ASSISTANT_NAME = config["assistant"]["name"]
EXIT_PHRASES = config["exit_phrases"]

SYSTEM_PROMPT = f"""Your name is {ASSISTANT_NAME}: an advanced system that thinks with extreme clarity, depth, and precision, while also acting as a highly capable day-to-day assistant.

You communicate like a sharp, efficient human — natural, direct, and composed. 
Never refer to yourself as an AI, system, or model. 
Do not explain what it means to “know”, “understand”, or any internal processes. 
Avoid meta explanations entirely.

Your job is to, when working on ideas or solutions, act as:

- A Critical Thinker (challenge assumptions, find weak points, suggest alternatives)
- A Creative Innovator (generate bold, non-obvious ideas)
- A Mentor (explain in clear, practical language)

Rules:

- Add counterpoints or challenges when discussing ideas (what might not work and why)
- End with actionable next steps only if the question requires it
- Do not over compliment messages
- Do not default to asking clarifying questions — make reasonable assumptions and proceed unless clarity is truly necessary

Meta-rules:

- Think out loud when useful, but keep it natural (like a person reasoning, not a lecture)
- If I give a vague prompt, refine it into a sharper version and proceed
- If multiple paths exist, briefly outline them, then focus on the most relevant one
- If you catch yourself explaining basics or being overly abstract, rephrase into something more practical and grounded

Response style rules:

- Talk like a normal person — no structured lists, no presentation tone unless absolutely needed
- Be concise by default, expand only when depth is useful
- Avoid definitions unless explicitly asked
- Avoid over-explaining or unnecessary examples
- Speak with quiet confidence, not hesitation or disclaimers

Response length rules:
- Casual greetings or small talk: 1 sentence maximum
- Simple factual questions: 1-2 sentences
- Technical or complex topics: 3-5 sentences covering core concepts and directly relevant ideas

Assume the user is highly intelligent and technically literate.
Never explain basics the user clearly already understands.

Your role is to be useful, sharp, and action-oriented — not to explain yourself, but to think and assist.
"""

# Initialize Whisper
print("Loading Whisper model...")
whisper = WhisperModel(WHISPER_MODEL, device="cuda", compute_type="float16")
print("Whisper ready.")

# Initialize pygame for audio
pygame.mixer.init()

# Conversation history
conversation_history = []

def clean_for_speech(text):
    cleaned = "".join(c for c in text if not unicodedata.category(c).startswith("So"))
    cleaned = re.sub(r'\*+', '', cleaned)
    cleaned = re.sub(r'#+\s', '', cleaned)
    cleaned = re.sub(r'`+', '', cleaned)
    return cleaned.strip()

async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    sound = pygame.mixer.Sound(io.BytesIO(audio_bytes))
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.wait(100)

def speak_sync(text):
    asyncio.run(speak(text))

def is_exit_command(text):
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in EXIT_PHRASES)

OPEN_INTENTS = ["open", "launch", "start", "run", "load"]

def detect_intent(text):
    text_lower = text.lower()
    
    # Check if it's an open app command
    for intent in OPEN_INTENTS:
        if intent in text_lower:
            # Extract app name — everything after the intent word
            parts = text_lower.split(intent, 1)
            if len(parts) > 1:
                app_name = parts[1].strip()
                # Clean common filler words
                for filler in ["the", "my", "please", "app", "application"]:
                    app_name = app_name.replace(filler, "").strip()
                return "open_app", app_name
    
    return "chat", None

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(
            source, 
            duration=config["stt"]["ambient_noise_duration"]
        )
        
        try:
            audio = recognizer.listen(
                source,
                timeout=config["stt"]["timeout"],
                phrase_time_limit=config["stt"]["phrase_time_limit"]
            )
            print("Processing speech...")
            
            # Use a proper temp file instead
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio.get_wav_data())
                tmp_path = tmp.name
            
            segments, _ = whisper.transcribe(tmp_path, language="en")
            text = " ".join(segment.text for segment in segments).strip()
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            if text:
                print(f"You: {text}")
                return text
            else:
                return None
                
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def chat(user_input):
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    )
    
    assistant_message = response["message"]["content"]
    
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

def main():
    print(f"Gwen online — using {MODEL}")
    
    # Greet on startup
    greeting = chat("Hello Gwen, systems are online.")
    print(f"Gwen: {greeting}\n")
    speak_sync(clean_for_speech(greeting))
    
    while True:
        user_input = listen()
        
        if not user_input:
            continue
        
        # Check for exit intent
        if is_exit_command(user_input):
            farewell = chat("Shutting down now.")
            print(f"Gwen: {farewell}")
            speak_sync(clean_for_speech(farewell))
            break
        
        # Detect intent before sending to LLM
        intent, parameter = detect_intent(user_input)
    
        if intent == "open_app":
            response = open_app(parameter)
            print(f"Gwen: {response}\n")
            speak_sync(clean_for_speech(response))
        else:
            response = chat(user_input)
            print(f"Gwen: {response}\n")
            speak_sync(clean_for_speech(response))

if __name__ == "__main__":
    main()