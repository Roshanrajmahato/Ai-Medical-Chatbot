from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from src.brain_of_doctor import encode_image, analyze_image_with_query
from src.voice_of_patient import transcribe_with_groq
from src.voice_of_doctor import text_to_speech_with_elevenlabs,text_to_speech_with_gtts
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        audio_file = request.files.get('audio')
        image_file = request.files.get('image')

        audio_path, image_path = None, None

        if audio_file:
            audio_filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            audio_file.save(audio_path)

        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)

        # Transcribe
        stt_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_path,
            stt_model="whisper-large-v3"
        )

        # Analyze Image
        if image_path:
            encoded = encode_image(image_path)
            query = system_prompt + stt_output
            doctor_response = analyze_image_with_query(query=query, encoded_image=encoded, model="meta-llama/llama-4-scout-17b-16e-instruct")
        else:
            doctor_response = "No image provided for me to analyze"

        # Generate TTS
        # Safe absolute output path
        output_audio_path = os.path.abspath(os.path.join("static", "outputs", "final.mp3"))

        # Ensure file is not locked before writing
        if os.path.exists(output_audio_path):
            try:
                os.remove(output_audio_path)
            except PermissionError:
                print("Audio file is currently in use. Please close anything using it.")

        # Save audio
        text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_path)

        return render_template("index.html",
                               stt_output=stt_output,
                               doctor_response=doctor_response,
                               audio_output="static/outputs/final.mp3")

    return render_template("index.html")


@app.route('/outputs/<filename>')
def serve_output_audio(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
