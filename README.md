# Interview Evaluation System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Detailed Component Breakdown](#detailed-component-breakdown)
   - [app.py](#apppy)
   - [speechrec.py](#speechrecpy)
   - [rag.py](#ragpy)
   - [intervieweval.py](#intervalevalpy)
   - [index.html](#indexhtml)
6. [Setup and Installation](#setup-and-installation)
7. [Usage Guide](#usage-guide)
8. [Contributing Guidelines](#contributing-guidelines)
9. [Troubleshooting](#troubleshooting)
10. [Future Improvements](#future-improvements)

## Project Overview
The Interview Evaluation System is a sophisticated web-based application designed to automate and enhance the interview process. It leverages cutting-edge technologies in speech recognition, natural language processing, and machine learning to transcribe interview questions and answers, generate ideal responses, and provide comprehensive evaluations of interviewee performance.

## Key Features
1. Real-time speech-to-text conversion for capturing interview dialogue
2. Retrieval-Augmented Generation (RAG) for producing context-aware ideal answers
3. Automated answer evaluation using ROUGE scores and LLM-based assessment
4. Interactive conversation history tracking
5. Detailed debug logging for system diagnostics and troubleshooting

## Technology Stack
- **Backend**: Python 3.8+, Flask 2.0+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Speech Recognition**: SpeechRecognition library
- **Natural Language Processing**: Langchain, Groq API
- **Audio Processing**: FFmpeg
- **Text Similarity**: ROUGE
- **Asynchronous Programming**: asyncio

## Project Structure
```
interview_evaluation_system/
│
├── app.py                 # Main Flask application
├── speechrec.py           # Speech recognition module
├── rag.py                 # Retrieval-Augmented Generation module
├── intervieweval.py       # Answer evaluation module
├── requirements.txt       # Python dependencies
│
├── templates/
│   └── index.html         # Main frontend interface
│
├── static/
│   ├── css/
│   │   └── styles.css     # Custom CSS (if separated from index.html)
│   └── js/
│       └── main.js        # Custom JavaScript (if separated from index.html)
│
└── temp/                  # Temporary directory for audio files (created at runtime)
```

## Detailed Component Breakdown

### app.py
This is the core of our Flask application, orchestrating all components and handling HTTP requests.

Key Functions:
- `process_audio()`: Handles audio file uploads, coordinates transcription, answer generation, and evaluation.
  ```python
  @app.route('/process_audio', methods=['POST'])
  def process_audio():
      # ... (file handling and audio conversion)
      text = speech_to_text(wav_path)
      if is_question:
          return jsonify({'text': text})
      else:
          ideal_answer = rag_generator.generate_answer(question)
          evaluation = asyncio.run(scorer.score_answer(question, ideal_answer, text))
          return jsonify({'text': text, 'evaluation': evaluation})
  ```
  This function demonstrates how we integrate speech recognition, RAG, and evaluation components.

- `convert_to_wav()`: Utilizes FFmpeg to convert uploaded audio to WAV format.
  ```python
  def convert_to_wav(input_path, output_path):
      command = [FFMPEG_PATH, '-i', input_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_path]
      result = subprocess.run(command, check=True, capture_output=True, text=True)
  ```
  This function is crucial for ensuring audio compatibility across different systems.

### speechrec.py
Handles the speech-to-text conversion using the SpeechRecognition library.

Key Function:
- `speech_to_text()`: Converts audio file to text.
  ```python
  def speech_to_text(audio_file_path):
      recognizer = sr.Recognizer()
      with sr.AudioFile(audio_file_path) as source:
          audio = recognizer.record(source)
      try:
          return recognizer.recognize_google(audio)
      except sr.UnknownValueError:
          return "Speech recognition could not understand the audio"
      except sr.RequestError as e:
          return f"Could not request results from speech recognition service; {e}"
  ```
  This function encapsulates error handling for common speech recognition issues.

### rag.py
Implements the Retrieval-Augmented Generation system for producing ideal answers.

Key Class:
- `RAGAnswerGenerator`: Manages the RAG process.
  ```python
  class RAGAnswerGenerator:
      def __init__(self, knowledge_base_dir, groq_api_key):
          # ... (initialization)

      def _create_vectorstore(self):
          # ... (create FAISS vectorstore from knowledge base)

      def _create_qa_chain(self):
          # ... (set up ConversationalRetrievalChain)

      def generate_answer(self, question):
          return self.qa_chain.run(question)
  ```
  This class demonstrates how we integrate FAISS for efficient similarity search and Groq API for language model inference.

### intervieweval.py
Handles the evaluation of interviewee answers against ideal responses.

Key Class:
- `AnswerComparisonScorer`: Manages the scoring process.
  ```python
  class AnswerComparisonScorer:
      def __init__(self, groq_api_key):
          # ... (initialization)

      async def llm_evaluation(self, question, ideal_answer, actual_answer):
          # ... (perform LLM-based evaluation)

      def compute_rouge_scores(self, ideal_answer, actual_answer):
          # ... (calculate ROUGE scores)

      async def score_answer(self, question, ideal_answer, actual_answer):
          rouge_scores = self.compute_rouge_scores(ideal_answer, actual_answer)
          llm_evaluation = await self.llm_evaluation(question, ideal_answer, actual_answer)
          # ... (combine scores and return evaluation)
  ```
  This class showcases the use of both traditional metrics (ROUGE) and AI-based evaluation using Groq API.

### index.html
Provides the user interface and client-side logic for the application.

Key JavaScript Functions:
- `startRecording()`: Initiates audio recording.
- `stopRecording()`: Stops recording and sends audio to the server.
- `updateButtonState()`: Manages UI state based on recording status.
- `addToConversationHistory()`: Updates the conversation display with new Q&A pairs.

## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/your-repo/interview-evaluation-system.git
   cd interview-evaluation-system
   ```
2. Install FFmpeg on your system (visit https://ffmpeg.org/download.html for instructions)
3. Set up a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set the GROQ_API_KEY environment variable:
   ```
   export GROQ_API_KEY="your-api-key-here"
   ```
6. Run the application:
   ```
   python app.py
   ```

## Usage Guide
1. Access the application by navigating to `http://localhost:5000` in your web browser.
2. Click "Start Question" to begin recording an interview question.
3. Click "Stop Question" when finished. The transcribed question will appear.
4. Click "Start Answer" to record the interviewee's response.
5. Click "Stop Answer" to end recording. The system will process and evaluate the answer.
6. View the evaluation results and conversation history on the page.

## Contributing Guidelines
1. Fork the repository and create a new branch for your feature or bug fix.
2. Ensure your code follows PEP 8 style guide for Python code.
3. Write unit tests for new features using pytest.
4. Update documentation, including this README, as necessary.
5. Submit a pull request with a clear description of your changes.

## Troubleshooting
- If you encounter audio-related issues, ensure FFmpeg is correctly installed and accessible in your system PATH.
- For speech recognition errors, check your microphone settings and internet connection.
- If you face Groq API issues, verify your API key and check Groq's service status.

## Future Improvements
1. Implement user authentication and session management for secure, multi-user support.
2. Add support for multiple interview types or domains with customizable evaluation criteria.
3. Enhance error handling with more informative user feedback.
4. Optimize performance for handling longer interviews and larger knowledge bases.
5. Implement a more sophisticated frontend framework (e.g., React, Vue.js) for improved interactivity.
6. Integrate with popular video conferencing platforms for remote interview support.

For any questions or issues, please open an issue in the GitHub repository or contact the maintainers directly.
