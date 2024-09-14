import speech_recognition as sr
import pyaudio

def speech_to_text(duration=5, phrase_time_limit=None):
    """
    Capture speech from the microphone and convert it to text.
    
    :param duration: Maximum number of seconds to listen for (default 5)
    :param phrase_time_limit: Maximum number of seconds for a phrase (default None)
    :return: Recognized text as a string
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        
        try:
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=phrase_time_limit)
            print("Processing speech...")
            
            text = recognizer.recognize_google(audio)
            print("Recognized text:", text)
            return text
        
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
            return ""

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
