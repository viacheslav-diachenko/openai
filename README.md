# openai
A repo for Open AI agents testing

## Text-to-Speech Web Interface

This project provides a small Flask application for converting text (from direct input or uploaded PDF/EPUB/TXT files) into speech using Google Cloud Text-to-Speech. Users supply their service account JSON key which is used directly by the backend.

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser.

### Features

- Upload PDF, EPUB or TXT files or paste text directly.
- Choose available Ukrainian voices and adjust speaking rate, pitch and volume.
- Generates an MP3 file using Google Cloud Text-to-Speech that can be played or downloaded.

No uploaded text, audio or credentials are stored on the server.
