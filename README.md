# 🧠 Voice to Text

A lightweight, voice-activated interview assistant written in pure Python. This tool uses your microphone to capture spoken answers, transcribes them, and structures the output as an interview transcript.

## 🎯 Features

- 🎙️ Voice input via microphone (using `speech_recognition`)
- ✉️ Basic transcription cleanup (e.g., converts “at the rate” to `@`)
- 🧾 Candidate registration: name, address, number, email
- 🗣️ Role-specific interview question
- 📄 Console-based transcript generation

## 📦 Requirements

Python 3.8 or higher

Install dependencies:

```bash
pip install -r requirements.txt
