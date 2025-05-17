# openai
A repo for Open AI agents testing

## Text-to-Speech Web Interface

This example `app.py` provides a simple Streamlit interface for converting text
from PDF, EPUB, or TXT files into speech using Google Cloud Text-to-Speech.
Users supply their own API key which is used directly with Google's REST API.

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```

### Features

- Upload PDF, EPUB or TXT files.
- Extracts text from the uploaded document.
- Choose available Ukrainian voices and adjust speaking rate and pitch.
- Generate and download an MP3 file using Google Cloud Text-to-Speech.

No uploaded text or generated audio is stored on the server.
