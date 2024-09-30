from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
import subprocess
import asyncio
from speechrec import speech_to_text
from rag import RAGAnswerGenerator
from intervieweval import AnswerComparisonScorer

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the app knows where to find templates
app.template_folder = 'templates'

# Create a 'temp' directory if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

# Replace this path with the actual path to ffmpeg
FFMPEG_PATH = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"

# Initialize your components
rag_generator = RAGAnswerGenerator("RAG", os.getenv("GROQ_API_KEY"))
scorer = AnswerComparisonScorer(os.getenv("GROQ_API_KEY"))

def convert_to_wav(input_path, output_path):
    try:
        command = [FFMPEG_PATH, '-i', input_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_path]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Converted {input_path} to {output_path}")
        logging.debug(f"FFmpeg output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting audio: {e}")
        logging.error(f"FFmpeg error output: {e.stderr}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join(TEMP_DIR, filename)
        wav_path = os.path.join(TEMP_DIR, 'converted_audio.wav')
        
        try:
            file.save(input_path)
            logging.info(f"Audio file saved successfully to {input_path}")
            
            # Convert audio to WAV
            convert_to_wav(input_path, wav_path)
            
            # Process the audio file
            text = speech_to_text(wav_path)
            logging.info(f"Speech recognized: {text}")
            
            is_question = request.form.get('is_question') == 'true'
            
            if is_question:
                return jsonify({'text': text})
            else:
                # Generate ideal answer and evaluate
                question = request.form.get('question')
                ideal_answer = rag_generator.generate_answer(question)
                
                # Use asyncio to run the async score_answer method
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                evaluation = loop.run_until_complete(scorer.score_answer(question, ideal_answer, text))
                loop.close()
                
                return jsonify({
                    'text': text,
                    'evaluation': evaluation
                })
        except Exception as e:
            logging.error(f"Error processing audio: {str(e)}")
            return jsonify({'error': f"Error processing audio: {str(e)}"}), 500
        finally:
            # Clean up the temporary files
            for path in [input_path, wav_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                        logging.info(f"Temporary file {path} removed")
                    except Exception as e:
                        logging.error(f"Failed to remove temporary file: {e}")

if __name__ == '__main__':
    app.run(debug=True)