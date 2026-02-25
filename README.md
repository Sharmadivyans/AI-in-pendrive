🛠️ Project JARVIS-on-a-Stick

A self-contained, portable, offline AI Assistant that runs directly from a USB drive.

This project provides a high-level architecture and configuration guide for building a fully functional AI assistant capable of:

System automation

Voice interaction

Natural language reasoning

…all without installing anything on the host machine.

🏗️ 1. Portable Environment Architecture

To run Python without installation, the system bypasses registry and environment dependencies using an embedded setup.

Core Setup

Base Runtime: WinPython or Python Embedded Package (Windows)

Portable Git: Included for updates and dependency handling

Relative Pathing:
All scripts rely on:

os.path.dirname(__file__)
# or
pathlib.Path.cwd()

This ensures compatibility regardless of USB drive letter (D:, F:, etc.).

🧠 2. Local Brain: Lightweight LLMs

Models are selected for high intelligence-to-size efficiency and CPU compatibility via GGUF quantization.

Model	Size	Best For
Phi-3 Mini (3.8B)	~2.3 GB	Reasoning & Logic
Llama-3-8B (4-bit)	~4.7 GB	Creative Writing & Chat
TinyLlama-1.1B	~700 MB	Ultra-fast, low-resource tasks
Gemma-2B	~1.6 GB	General knowledge & safety
⚙️ 3. Inference & Orchestration

The inference engine converts model weights into actual responses.

Options

Llama.cpp

Industry standard for local CPU inference

Highly portable

Compile once → run executable via Python subprocess

Ollama (Portable Mode)

Models stored on USB via:

set OLLAMA_MODELS=%~dp0\Models

GPT4All

Python SDK

Minimal setup overhead

Handles local execution automatically

🤖 4. Automation & Tool Use

This is where the assistant becomes “JARVIS” — moving beyond chat into action.

Python Automation Stack

subprocess / os → Launch apps (Chrome, Word, etc.)

pywinauto → Deep Windows UI automation

PyAutoGUI → Mouse/keyboard control when APIs aren’t available

Function Calling Framework (ReAct Pattern)

Prompting: LLM receives list of available tools/functions

JSON Output: Example:

{"action":"launch_app","params":"Word"}

Local Execution: Python wrapper parses JSON and runs the action.

🎙️ 5. Voice Interaction (Offline)

Fully private voice support with zero cloud dependency.

Speech-to-Text (STT)

Vosk

Lightweight (~50MB models)

Completely offline

Text-to-Speech (TTS)

pyttsx3

Uses native OS voices

Fast, zero latency

💾 6. Hardware Requirements

Since models load directly from USB, storage speed is critical.

Minimum

USB 3.0 / 3.1

32GB storage

Recommended

USB 3.2 Gen 2 or Portable NVMe SSD

Read speeds > 400 MB/s

64GB+ storage for multiple models

⚠️ Running models from USB 2.0 will cause significant loading delays.

🚀 Quick Start (Architecture Layout)
/USB-Drive
│
├── /Python-Embedded/     # Portable Python binaries
├── /Models/              # GGUF model files
├── /Workspace/           # Automation scripts
├── /Binaries/            # llama.cpp, ffmpeg, etc.
└── launch_jarvis.bat     # Entry point
📜 Roadmap

 Implement local RAG (offline document memory)

 Add lightweight Flask/FastAPI GUI

 Integrate wake-word detection (pvporcupine)

🧩 Vision

JARVIS-on-a-Stick is designed to be:

Portable

Private

Offline

System-level capable

Zero-installation

A true plug-and-play personal AI assistant.

🧱 Week 1 — Foundations & Environment

Goal: Set up the portable USB environment.

Tasks

Format a high-speed USB drive (USB 3.2 Gen 2 recommended, NTFS filesystem).

Download and extract WinPython or Python Embedded into:

/env

Create a launch.bat script to verify everything runs without system Python.

Ensure all paths are relative so the setup works on any drive letter.

Hardware Check

Confirm drive read speed is at least 300 MB/s for fast model loading.

🧠 Week 2 — Intelligence & Inference

Goal: Run a local LLM entirely from USB.

Tasks

Install llama-cpp-python (CPU version) inside the portable environment.

Download a GGUF model such as:

Phi-3 Mini

Llama-3.2-3B

(Use 4-bit or 5-bit quantization for performance.)

Build a basic script that:

Takes text input

Sends it to the model

Returns a generated response

🎙️ Week 3 — Voice & Function Calling

Goal: Give JARVIS “ears” and “hands.”

Tasks

Integrate Vosk for fully offline speech-to-text.

Implement Function Calling logic.

Example functions:

open_app(name)
system_status()

Prompt the LLM to output structured JSON instead of plain text.

Example:

{"task":"launch","target":"chrome"}

Build a Python dispatcher that parses JSON and executes actions.

🧩 Week 4 — Synthesis & UI

Goal: Polish the user experience and finalize the JARVIS persona.

Tasks

Add pyttsx3 for offline text-to-speech responses.

Create either:

A wake-word listener, or

A lightweight terminal UI

Optimize startup by pre-loading the model into RAM.

Perform testing on multiple guest computers.

💾 Hardware Recommendations

Your USB drive speed heavily impacts performance.

Component	Minimum	Recommended
Drive Interface	USB 3.0	USB 3.1 / 3.2 Gen 2
Read Speed	100 MB/s	400+ MB/s (NVMe USB)
Capacity	32 GB	64–128 GB
Host RAM	8 GB	16 GB+
🚀 Future Roadmap

 RAG: Add local vector memory using ChromaDB for document recall.

 Vision: Integrate portable webcam support for object recognition.

 Agent Memory: Persistent conversation history stored locally.

 Web UI: Lightweight Flask/FastAPI dashboard.
