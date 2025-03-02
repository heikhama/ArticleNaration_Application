"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import jsonify, render_template, request, send_file
from ArticleNaration_Application import app
from TTS.api import TTS
import os
import ollama

from ArticleNaration_Application.templates.textlanguageconversion import OllamaChat

OUTPUT_DIR = 'Results'
os.makedirs(OUTPUT_DIR, exist_ok=True)
tts = TTS("CUSTOM_MODEL_DIR/tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    """Renders the imageGenerate page."""
    return render_template(
        'index.html',
        title='Text-to-Speech',
        year=datetime.now().year,
        message='Convert the Given text To Audio Wav'
        
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

### Generate Audio using TTS



@app.route('/generate-speech', methods=['POST'])
def generate_speech():     
    translateLanguage = OllamaChat(model="llama3.1")  # Replace with your model name

    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'male')
        language = data.get('language', 'english')
        #Use part of the text and the current datetime for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_part = text[:20].replace(" ", "_")  # First 20 chars of text, replacing spaces with underscores
        output_path = f"{OUTPUT_DIR}/{filename_part}_{timestamp}.wav"

        # tts = TTS("CUSTOM_MODEL_DIR/tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
        # Extract text input
        
        if not text:
            return jsonify({"error": "Missing text input."}), 400
        
        if not language:
            return jsonify({"error": "Missing Language Option."}), 400
        
        if(language == "english"):
            translated_text = text
        else:
            translated_text = translateLanguage.translate_text(text, language)
            
        print(f"Translated Text to {language}:", translated_text)
        
        # newprompt = f"Translate the text: {text} to {language}"
        # responseMessage = translateLanguage.translate_language(newprompt)
        # print(responseMessage)

        #Assigning code for tts input
        if(language == "english"): 
            language =  "en"            
        if(language == "hindi"): 
            language =  "hi"
        if(language == "french"): 
            language =  "fr"
        if(language == "russian"): 
            language =  "ru"

        # Default speaker WAV file (you can change this logic)
         # speaker_wav = "data/harvard.wav"
        if(voice == "enmale"):
            speaker_wav = "VoiceSample/male/harvard.wav"
        if(voice == "enIndmale"):
            speaker_wav = "VoiceSample/male/myvoice.wav" 
        if(voice == "enfemale"):
            speaker_wav = "VoiceSample/female/female_spoken_en.wav" 
        if(voice == "ruFemale"):
            speaker_wav = "VoiceSample/female/russian-female.wav" 
        if(voice == "enIndian"):
            speaker_wav = "VoiceSample/female/generic_female_en.wav" 
        
        if not speaker_wav:
            return jsonify({"error": "Missing speaker WAV file."}), 400



        # Generate speech and save to static folder        

        tts.tts_to_file(text=translated_text, file_path=output_path, speaker_wav=speaker_wav, language=language)

        # Return the path to the frontend
        return jsonify({
            "message": "Speech generated successfully.", 
            "audio_path": f"/{output_path}",
            "responseMessage":translated_text
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-audio/<filename>', methods=['GET'])
def get_image(filename):
    corrected_folder = os.path.join(os.getcwd(), OUTPUT_DIR)
    file_path = os.path.join(corrected_folder, filename)

    # Debug the file path
    if not os.path.exists(file_path):
        return jsonify({"error": f"File not found: {file_path}"}), 404

    return send_file(file_path, as_attachment=True, mimetype='audio/wav')