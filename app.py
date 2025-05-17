import base64
import io
import requests

import streamlit as st
from pdfminer.high_level import extract_text as extract_pdf_text
from ebooklib import epub
import ebooklib


def extract_text_from_epub(uploaded_file: io.BytesIO) -> str:
    book = epub.read_epub(uploaded_file)
    text_items = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text_items.append(item.get_content().decode('utf-8'))
    return '\n'.join(text_items)


def extract_text(file) -> str:
    if file.name.lower().endswith('.pdf'):
        return extract_pdf_text(file)
    elif file.name.lower().endswith('.epub'):
        return extract_text_from_epub(file)
    else:
        return file.read().decode('utf-8')


def list_voices(api_key: str):
    url = f"https://texttospeech.googleapis.com/v1/voices?languageCode=uk-UA&key={api_key}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return [v['name'] for v in data.get('voices', [])]
    return []


def synthesize_speech(text: str, api_key: str, voice: str, speed: float, pitch: float) -> bytes:
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": "uk-UA",
            "name": voice
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": speed,
            "pitch": pitch
        }
    }
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        audio_content = resp.json()['audioContent']
        return base64.b64decode(audio_content)
    else:
        st.error(f"Error: {resp.text}")
        return b""


def main():
    st.title("Text-to-Speech Converter")

    api_key = st.text_input("Google Cloud API key", type="password")

    uploaded_file = st.file_uploader("Upload PDF, EPUB or TXT", type=["pdf", "epub", "txt"])

    text = ""
    if uploaded_file is not None:
        text = extract_text(uploaded_file)
        st.text_area("Extracted Text", value=text, height=200)

    if api_key:
        voices = list_voices(api_key)
    else:
        voices = []
    voice = st.selectbox("Voice", voices)
    speed = st.slider("Speaking rate", 0.25, 4.0, 1.0, 0.05)
    pitch = st.slider("Pitch", -20.0, 20.0, 0.0, 0.1)

    if st.button("Synthesize"):
        if not api_key:
            st.error("API key required")
        elif not text:
            st.error("No text to synthesize")
        else:
            audio_bytes = synthesize_speech(text, api_key, voice, speed, pitch)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')
                b64 = base64.b64encode(audio_bytes).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Download MP3</a>'
                st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
