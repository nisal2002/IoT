import speech_recognition as sr # type: ignore
import pyaudio # type: ignore
import wave
import time
import os
import json
import requests # type: ignore

def record_audio(filename="recording.wav", duration=5, sample_rate=44100, chunk=1024):
    """
    Record audio from microphone
    
    Parameters:
    - filename: Output audio file
    - duration: Recording duration in seconds
    - sample_rate: Audio sample rate
    - chunk: Audio chunk size
    
    Returns:
    - Path to recorded audio file
    """
    print(f"Recording will start in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print(f"Recording for {duration} seconds...")
    
    audio_format = pyaudio.paInt16
    channels = 1
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    frames = []
    
    # Record for the specified duration
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording finished!")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the recorded audio as WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return filename

def speech_to_text(audio_file, language="si-LK"):
    """
    Convert speech to text using Google Speech Recognition
    
    Parameters:
    - audio_file: Path to audio file
    - language: Language code (si-LK for Sinhala)
    
    Returns:
    - Recognized text
    """
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        # Get audio data
        audio_data = recognizer.record(source)
        
        # Use Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def convert_to_singlish(unicode_text):
    """
    Convert Sinhala Unicode text to Singlish using the API (reversed operation)
    Note: This might not be fully accurate as the conversion is usually lossy
    """
    url = 'https://singlish.kdj.lk/api.php'
    data = {
        'text': unicode_text,
        'inputType': 'unicode',
        'format': 'singlish'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result['status'] == 'success':
            return result['result']
        else:
            raise Exception(result.get('message', 'Conversion failed'))
    except Exception as e:
        print(f"Could not convert to Singlish: {e}")
        return None

def main():
    print("=== Sinhala Speech to Text Converter ===")
    
    while True:
        # Ask for recording duration
        try:
            duration = float(input("Enter recording duration in seconds (default: 5): ") or 5)
        except ValueError:
            print("Invalid input. Using default 5 seconds.")
            duration = 5
        
        # Record audio
        audio_file = record_audio(duration=duration)
        
        # Convert speech to text
        print("Processing speech...")
        recognized_text = speech_to_text(audio_file)
        
        print("\nRecognized Text (Sinhala):")
        print(recognized_text)
        
        # Try to convert to Singlish (optional)
        singlish_text = convert_to_singlish(recognized_text)
        if singlish_text:
            print("\nConverted to Singlish:")
            print(singlish_text)
        
        # Ask if user wants to continue
        choice = input("\nDo you want to record again? (y/n): ")
        if choice.lower() != 'y':
            break
        print("\n" + "-" * 40 + "\n")

        if choice.lower() == 'n':
            break

    #Vihanga -  Change this according to your will. 
    print("Thank you for using the Sinhala Speech to Text Converter!")

if __name__ == "__main__":
    main()