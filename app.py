from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
import subprocess
import asyncio
from speechrec import speech_to_text
from rag import RAGAnswerGenerator
from intervieweval import AnswerComparisonScorer
import uuid


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

# def cleanup_temp_directory():
#     try:
#         if os.path.exists(TEMP_DIR):
#             shutil.rmtree(TEMP_DIR)
#             logging.info(f"Existing temp directory removed: {TEMP_DIR}")
#         os.makedirs(TEMP_DIR, exist_ok=True)
#         logging.info(f"New temp directory created: {TEMP_DIR}")
#     except Exception as e:
#         logging.error(f"Error during temp directory cleanup: {str(e)}")


def convert_to_wav(input_path, output_path, timeout=30):
    try:
        logging.info(f'Starting conversion process. Input: {input_path}, Output: {output_path}')
        logging.info(f'FFmpeg path: {FFMPEG_PATH}')
        
        if not os.path.exists(input_path):
            logging.error(f"Input file does not exist: {input_path}")
            return False

        command = [FFMPEG_PATH, '-i', input_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_path]
        logging.info(f"Executing command: {' '.join(command)}")
        
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
        
        logging.info(f"Conversion successful. FFmpeg output: {result.stdout}")
        logging.info(f"Converted {input_path} to {output_path}")
        return True
    except subprocess.TimeoutExpired:
        logging.error(f"FFmpeg conversion timed out after {timeout} seconds")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg conversion failed. Error: {e}")
        logging.error(f"FFmpeg stderr: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during conversion: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    logging.info("Received audio processing request")
    if 'audio' not in request.files:
        logging.error("No audio file in request")
        return jsonify({'error': 'No audio file'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        logging.error("Empty filename")
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}_{original_filename}"
        input_path = os.path.join(TEMP_DIR, filename)
        wav_filename = f"{unique_id}_converted_audio.wav"
        wav_path = os.path.join(TEMP_DIR, wav_filename)
        
        try:
            file.save(input_path)
            logging.info(f"Audio file saved successfully to {input_path}")
            
            # Convert audio to WAV
            conversion_success = convert_to_wav(input_path, wav_path)
            if not conversion_success:
                logging.error("Audio conversion failed")
                return jsonify({'error': 'Audio conversion failed'}), 500
            
            # Process the audio file
            logging.info("Starting speech recognition")
            text = speech_to_text(wav_path)
            logging.info(f"Speech recognized: {text}")
            
            is_question = request.form.get('is_question') == 'true'
            
            if is_question:
                logging.info("Processing as a question")
                return jsonify({'text': text})
            else:
                logging.info("Processing as an answer")
                # Generate ideal answer and evaluate
                question = request.form.get('question')
                logging.info(f"Generating ideal answer for question: {question}")
                ideal_answer = rag_generator.generate_answer(question)
                logging.info("Ideal answer generated")
                
                logging.info("Starting answer evaluation")
                # Use asyncio to run the async score_answer method
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                evaluation = loop.run_until_complete(scorer.score_answer(question, ideal_answer, text))
                loop.close()
                logging.info("Answer evaluation completed")
                
                return jsonify({
                    'text': text,
                    'evaluation': evaluation
                })
        except Exception as e:
            logging.error(f"Error processing audio: {str(e)}", exc_info=True)
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
    logging.info("Starting the Flask application")
    # cleanup_temp_directory()
    app.run(debug=True)