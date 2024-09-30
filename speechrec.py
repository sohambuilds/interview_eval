import speech_recognition as sr
import logging

def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            logging.info(f"Reading audio file: {audio_file_path}")
            audio = recognizer.record(source)
        
        logging.info("Attempting to recognize speech")
        text = recognizer.recognize_google(audio)
        logging.info(f"Speech recognized: {text}")
        return text
    except sr.UnknownValueError:
        logging.error("Speech recognition could not understand the audio")
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        logging.error(f"Could not request results from speech recognition service; {e}")
        return f"Could not request results from speech recognition service; {e}"
    except Exception as e:
        logging.error(f"Unexpected error in speech recognition: {e}")
        raise  # Re-raise the exception to be caught by the calling function

def capture_interview_qa():
    """
    Capture the interviewer's question and interviewee's answer using speech recognition.
    
    :return: A tuple containing the question and answer as strings
    """
    print("Capturing interviewer's question...")
    question = speech_to_text(duration=10)
    
    print("\nCapturing interviewee's answer...")
    answer = speech_to_text(duration=30)
    
    return question, answer

# Example usage
if __name__ == "__main__":
    question, answer = capture_interview_qa()
    print("\nInterviewer's question:", question)
    print("Interviewee's answer:", answer)
