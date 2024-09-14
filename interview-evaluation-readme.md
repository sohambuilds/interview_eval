# Interview Evaluation System

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)

## Introduction

This Interview Evaluation System is an advanced tool designed to automate and enhance the interview process. It combines speech recognition, Retrieval-Augmented Generation (RAG), and answer comparison to provide a comprehensive evaluation of interviewee responses.

Key features:
- Speech-to-text conversion for capturing interview questions and answers
- RAG-based system for generating ideal answers
- Sophisticated answer comparison and scoring mechanism
- Integration with Groq API for fast and efficient language processing

## System Requirements

- Python 3.8 or higher
- Operating System: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- Microphone for speech input
- Internet connection for API access

## Installation

1. Clone the repository or download the project files:
   ```
   git clone https://github.com/your-repo/interview-evaluation-system.git
   cd interview-evaluation-system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install speech_recognition pyaudio langchain groq chromadb sentence-transformers sklearn
   ```

   Note: If you encounter issues installing PyAudio, you may need to install additional system dependencies:
   - On Ubuntu/Debian:
     ```
     sudo apt-get install portaudio19-dev python-all-dev
     ```
   - On macOS:
     ```
     brew install portaudio
     ```
   - On Windows, you might need to download the PyAudio wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it manually:
     ```
     pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl
     ```

## Project Structure

The project consists of the following main files:

- `speech_recognition_module.py`: Handles speech-to-text conversion
- `rag_answer_generator.py`: Implements the RAG-based answer generation system
- `answer_comparison_scorer.py`: Compares and scores interviewee answers
- `interview_evaluation_pipeline.py`: Integrates all components into a cohesive pipeline

## Configuration

1. Groq API Key:
   - Sign up for a Groq account at https://console.groq.com/
   - Obtain your API key from the Groq console
   - Set the API key as an environment variable:
     ```
     export GROQ_API_KEY="your-groq-api-key"
     ```
     For Windows, use `set` instead of `export`

2. Knowledge Base:
   - Create a directory to store your knowledge base text files
   - Add relevant .txt files containing information about the interview topics
   - Update the `knowledge_base_dir` variable in `interview_evaluation_pipeline.py` with the path to your knowledge base directory

## Usage

1. Ensure your virtual environment is activated

2. Run the main script:
   ```
   python interview_evaluation_pipeline.py
   ```

3. Follow the on-screen prompts:
   - The system will ask for the interviewer's question (speak clearly into your microphone)
   - Then, it will ask for the interviewee's answer (again, speak clearly)
   - The system will process the inputs and provide an evaluation

4. Review the evaluation results, which include:
   - Final score
   - Similarity score
   - Detailed LLM evaluation

## Customization

1. Modifying the RAG system:
   - Edit `rag_answer_generator.py` to change the chunk size, overlap, or retrieval method
   - Experiment with different embedding models by changing the `model_name` in `HuggingFaceEmbeddings`

2. Adjusting the scoring system:
   - Modify the weights in the `score_answer` method of `answer_comparison_scorer.py`
   - Edit the evaluation prompt in `AnswerComparisonScorer.__init__` to change the criteria

3. Enhancing speech recognition:
   - Adjust the `duration` and `phrase_time_limit` parameters in `speech_recognition_module.py` for different listening behaviors

## Troubleshooting

1. Speech recognition issues:
   - Ensure your microphone is properly connected and selected as the default input device
   - Try adjusting your microphone volume or speaking more clearly
   - If you're in a noisy environment, consider using a noise-cancelling microphone

2. RAG system problems:
   - Verify that your knowledge base directory contains relevant .txt files
   - Check file permissions for the knowledge base directory

3. Groq API errors:
   - Confirm that your API key is correctly set as an environment variable
   - Check your internet connection
   - Verify that you have sufficient API credits in your Groq account

4. Scoring discrepancies:
   - Review the LLM evaluation output for insights into the scoring process
   - Adjust the scoring weights in `answer_comparison_scorer.py` if necessary

5. General issues:
   - Check the console for any error messages or warnings
   - Verify that all dependencies are correctly installed
   - Ensure you're using a compatible Python version

## Contributing

Contributions to this project are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

Please ensure your code adheres to the existing style and include appropriate tests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

For any additional questions or support, please open an issue on the GitHub repository or contact the maintainers directly.
