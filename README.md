# Gwen — AI Virtual Assistant
### Local AI-Powered Voice Assistant | Asistente de Voz con IA Local

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-black?logo=ollama)](https://ollama.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-AntoBeri-181717?logo=github)](https://github.com/AntoBeri)

---

## English

GWEN is a fully local, privacy-first AI voice assistant running entirely on your own computer. No cloud, no API keys, no data leaving your machine. Built with a modular architecture designed to grow from simple voice commands to advanced features.

### Features

- **100% Local** — everything runs on your machine, nothing is sent to the cloud
- **Voice Input** — speech to text powered by Faster-Whisper running on GPU
- **Voice Output** — natural sounding text to speech via Microsoft Edge TTS (en-GB-SoniaNeural)
- **Conversational AI** — context-aware conversations powered by a local LLM via Ollama
- **App Launcher** — open any application on your computer by voice command
- **Config-driven** — all settings managed through a single `config.json`, no hardcoded values
- **GPU Accelerated** — leverages CUDA for fast local inference

### Tech Stack

| Component | Technology |
|---|---|
| Local LLM | [Ollama](https://ollama.com) + Gemma 3 4B |
| Speech to Text | [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) |
| Text to Speech | [Edge-TTS](https://github.com/rany2/edge-tts) |
| Audio Playback | [Pygame](https://pygame.org) |
| GPU Acceleration | CUDA 12.x + PyTorch |
| Voice Detection | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) |

### Project Structure

```
ai_virtual_assistant/
├── assistant.py      # main loop, voice pipeline, conversation handling
├── tools.py          # executable actions (app launcher, future tools)
├── config.py         # config loader
├── config.json       # all settings — editable without touching code
└── README.md
```

### Requirements

- Python 3.11
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda, miniconda preferred)
- NVIDIA GPU with CUDA 12.x (recommended, CPU fallback available)
- Windows 10/11
- [Ollama](https://ollama.com) installed and running

### Setup

**1. Clone the repository**
```bash
git clone https://github.com/AntoBeri/ai_virtual_assistant.git
cd ai_virtual_assistant
```

**2. Create and activate a conda environment**
```bash
conda create -n ai-assistant python=3.11
conda activate ai-assistant
```

**3. Install PyTorch with CUDA support**
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```

**4. Install dependencies**
```bash
pip install ollama edge-tts pygame speechrecognition faster-whisper pyaudio
```

**5. Install and start Ollama, then pull the model**
```bash
ollama pull gemma3:4b
```

**6. Configure your settings**

Edit `config.json` to match your system — update app paths under the `"apps"` section to point to applications installed on your machine.

**7. Run**
```bash
python assistant.py
```

### Usage

Once running, simply speak to GWEN. Example commands:

- *"Open Chrome"*
- *"Open Spotify"*
- *"What is quantum entanglement?"*
- *"Goodbye"* — to shut down

### Configuration

All settings live in `config.json`. No code changes needed for common customizations:

```json
{
    "assistant": {
        "name": "Gwen",
        "voice": "en-GB-SoniaNeural",
        "model": "gemma3:4b",
        "whisper_model": "base"
    },
    "apps": {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    }
}
```

To add a new app, just add a new entry under `"apps"` — no code changes required.

---

## Español

GWEN es un asistente de voz con IA completamente local, enfocado en privacidad, que corre enteramente en tu propio hardware. Sin nube, sin API keys, sin datos saliendo de tu máquina. Construido con una arquitectura modular diseñada para crecer desde comandos de voz simples hasta control completo de hogar inteligente.

### Características

- **100% Local** — todo corre en tu máquina, nada se envía a la nube
- **Entrada por voz** — reconocimiento de voz con Faster-Whisper corriendo en GPU
- **Salida por voz** — texto a voz natural con Microsoft Edge TTS (en-GB-SoniaNeural)
- **IA Conversacional** — conversaciones con contexto impulsadas por un LLM local via Ollama
- **Lanzador de apps** — abre cualquier aplicación en tu computadora con comandos de voz
- **Configuración centralizada** — todas las opciones en un solo `config.json`, sin valores hardcodeados
- **Aceleración GPU** — usa CUDA para inferencia local rápida

### Stack Tecnológico

| Componente | Tecnología |
|---|---|
| LLM Local | [Ollama](https://ollama.com) + Gemma 3 4B |
| Voz a Texto | [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) |
| Texto a Voz | [Edge-TTS](https://github.com/rany2/edge-tts) |
| Reproducción de Audio | [Pygame](https://pygame.org) |
| Aceleración GPU | CUDA 12.x + PyTorch |
| Detección de Voz | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) |

### Estructura del Proyecto

```
ai_virtual_assistant/
├── assistant.py      # loop principal, pipeline de voz, manejo de conversación
├── tools.py          # acciones ejecutables (lanzador de apps, herramientas futuras)
├── config.py         # cargador de configuración
├── config.json       # todas las configuraciones — editables sin tocar el código
└── README.md
```

### Requisitos

- Python 3.11
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda, preferido miniconda)
- GPU NVIDIA con CUDA 12.x (recomendado, CPU disponible como fallback)
- Windows 10/11
- [Ollama](https://ollama.com) instalado y corriendo

### Instalación

**1. Clonar el repositorio**
```bash
git clone https://github.com/AntoBeri/ai_virtual_assistant.git
cd ai_virtual_assistant
```

**2. Crear y activar entorno conda**
```bash
conda create -n ai-assistant python=3.11
conda activate ai-assistant
```

**3. Instalar PyTorch con soporte CUDA**
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```

**4. Instalar dependencias**
```bash
pip install ollama edge-tts pygame speechrecognition faster-whisper pyaudio
```

**5. Instalar y ejecutar Ollama, luego descargar el modelo**
```bash
ollama pull gemma3:4b
```

**6. Configurar el sistema**

Edita `config.json` para que coincida con tu sistema — actualiza las rutas de apps bajo la sección `"apps"` para apuntar a las aplicaciones instaladas en tu máquina.

**7. Ejecutar**
```bash
python assistant.py
```

### Uso

Una vez corriendo, simplemente habla con GWEN. Ejemplos de comandos:

- *"Open Chrome"*
- *"Open Spotify"*
- *"What is quantum entanglement?"*
- *"Goodbye"* — para apagar

### Configuración

Todas las opciones viven en `config.json`. No se requieren cambios en el código para personalizaciones comunes:

```json
{
    "assistant": {
        "name": "Gwen",
        "voice": "en-GB-SoniaNeural",
        "model": "gemma3:4b",
        "whisper_model": "base"
    },
    "apps": {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    }
}
```

Para agregar una nueva app, solo añade una entrada en `"apps"` — sin cambios en el código.

---

## 🗺️ Roadmap

Features planned for future versions — *Características planeadas para versiones futuras*

### Phase 2 — System Control / Control del Sistema
- [ ] Volume and brightness control by voice
- [ ] System shutdown, restart, sleep via voice command
- [ ] Battery and system status queries

### Phase 3 — Information & Web / Información y Web
- [ ] Local web search integration
- [ ] Weather queries
- [ ] Real time news summaries

### Phase 4 — Memory & Personalization / Memoria y Personalización
- [ ] Persistent memory across sessions
- [ ] User preference learning
- [ ] Custom wake word detection ("Hey Gwen")

### Phase 5 — Smart Home / Hogar Inteligente
- [ ] Home Assistant integration
- [ ] Smart light control by voice
- [ ] Device state queries ("Are the lights on?")

### Phase 6 — Dedicated Hardware / Hardware Dedicado
- [ ] Migration to dedicated mini PC or SBC
- [ ] Always-on operation
- [ ] Upgraded local model with more VRAM

---

## Author / Autor

**Antonio Beristain** — [@AntoBeri](https://github.com/AntoBeri)

> *Built as a showcase of local AI integration, voice pipelines, and modular Python architecture.*
> *Construido como demostración de integración de IA local, pipelines de voz y arquitectura modular en Python.*
