from flask import Flask, render_template, request, jsonify, send_file
from pdfminer.high_level import extract_text as extract_pdf_text
from ebooklib import epub
import ebooklib
import io
import json
from google.cloud import texttospeech
from google.oauth2 import service_account

app = Flask(__name__)


def extract_text_from_epub(uploaded_file: io.BytesIO) -> str:
    book = epub.read_epub(uploaded_file)
    text_items = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text_items.append(item.get_content().decode("utf-8"))
    return "\n".join(text_items)


def extract_text(file) -> str:
    if file.filename.lower().endswith(".pdf"):
        return extract_pdf_text(file)
    elif file.filename.lower().endswith(".epub"):
        return extract_text_from_epub(file)
    else:
        return file.read().decode("utf-8")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tts", methods=["POST"])
def tts():
    api_key_json = request.form.get("apiKeyJson")
    if not api_key_json:
        return jsonify({"error": "API key JSON is required"}), 400

    try:
        key_data = json.loads(api_key_json)
        credentials = service_account.Credentials.from_service_account_info(key_data)
    except Exception:
        return jsonify({"error": "Invalid service account JSON"}), 400

    text = request.form.get("text", "")
    if not text and "file" in request.files:
        text = extract_text(request.files["file"])
    text = text.strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    language = request.form.get("language", "uk-UA")
    voice_name = request.form.get("voice", "uk-UA-Wavenet-A")
    try:
        speed = float(request.form.get("speed", 1.0))
        pitch = float(request.form.get("pitch", 0.0))
        volume_gain_db = float(request.form.get("volumeGainDb", 0.0))
    except ValueError:
        return jsonify({"error": "Invalid numeric parameters"}), 400

    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text[:5000])
    voice = texttospeech.VoiceSelectionParams(language_code=language, name=voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )

    try:
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(
        io.BytesIO(response.audio_content),
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="output.mp3",
    )


if __name__ == "__main__":
    app.run(debug=True)
