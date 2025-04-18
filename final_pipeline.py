import asyncio
import wave
import numpy as np
import os
import noisereduce as nr
from scipy.io import wavfile  # Add this import for saving WAV files
from googletrans import Translator  # Add this import for translation
import spacy  # Add spaCy import
import re  # For regular expressions

audio_folder_path = "audio_files"

def to_log(text):
    print(text)

def trigger_camera(platform_number):
    try:
        to_log(f"Triggering camera for platform {platform_number}")
        # Add your camera triggering logic here
        return True
    except Exception as e:
        to_log(f"Error triggering camera: {e}")
        return False

def detect_platform_number(text):
    # Load English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the text
    doc = nlp(text)
    
    # Pattern for platform numbers (e.g., "platform 3", "platform number 5")
    platform_pattern = re.compile(r'platform\s+(?:number\s+)?(\d+)', re.IGNORECASE)
    
    # First try regex pattern matching
    match = platform_pattern.search(text)
    if match:
        return match.group(1)
    
    # If no direct match, try NLP approach
    for ent in doc.ents:
        # Look for cardinal numbers near the word "platform"
        if ent.label_ == "CARDINAL":
            # Check if "platform" is within 3 tokens of the number
            platform_context = doc[max(0, ent.start - 3):min(len(doc), ent.end + 3)]
            if "platform" in platform_context.text.lower():
                return ent.text
    
    # Look for standalone numbers if they appear near "platform"
    for token in doc:
        if token.like_num:
            # Check surrounding context for the word "platform"
            context = doc[max(0, token.i - 3):min(len(doc), token.i + 3)]
            if "platform" in context.text.lower():
                return token.text
    
    return None

def translate_sinhala_to_english(text):
    translator = Translator()
    try:
        translation = translator.translate(text, src='si', dest='en')
        return translation.text
    except Exception as e:
        to_log(f"Translation error: {e}")
        return None

def save_wav(audio_data, sample_rate, output_path):
    # Ensure the audio data is scaled properly for int16 format
    audio_scaled = np.int16(audio_data * 32767)
    wavfile.write(output_path, sample_rate, audio_scaled)

def to_text(file_path):
    # Read the WAV file
    with wave.open(file_path, 'rb') as wav_file:
        # Get basic information about the WAV file
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        
        # Read the audio data
        audio_data = wav_file.readframes(n_frames)
        
        # Convert audio data to numpy array based on sample width
        dtype = np.int16 # Default for 2 bytes (16 bits)
        if sample_width == 1:
            dtype = np.uint8 # 8-bit unsigned
        elif sample_width == 4:
            dtype = np.int32 # 32-bit signed
        
        audio_array = np.frombuffer(audio_data, dtype=dtype)
        
        # If stereo, convert to mono by averaging channels
        if n_channels == 2:
            # Ensure the array length is even before reshaping
            if audio_array.size % 2 != 0:
                audio_array = audio_array[:-1] # Drop the last sample if odd
            audio_array = audio_array.reshape(-1, 2).mean(axis=1).astype(dtype)

        # Denoise the audio
        audio_float = audio_array.astype(np.float32) 
        denoised_audio = nr.reduce_noise(y=audio_float, sr=framerate)
        
        # Create output filename with _edited suffix
        file_name = os.path.splitext(file_path)[0]
        output_path = f"{file_name}_edited.wav"
        
        # Save the denoised audio
        save_wav(denoised_audio, framerate, output_path)
        to_log(f"Saved denoised audio to: {output_path}")

        # Convert speech to Sinhala text
        text_result = S2TSinhala.speech_to_text(denoised_audio, "si-LK")
        to_log(f"Sinhala text: {text_result}")
        
        # Translate and detect platform number
        if text_result:
            english_text = translate_sinhala_to_english(text_result)
            to_log(f"English translation: {english_text}")
            
            if english_text:
                platform_number = detect_platform_number(english_text)
                if platform_number:
                    to_log(f"Detected Platform Number: {platform_number}")
                    # Trigger the camera with the detected platform number
                    if trigger_camera(platform_number):
                        to_log(f"Successfully triggered camera for platform {platform_number}")
                    else:
                        to_log(f"Failed to trigger camera for platform {platform_number}")
                else:
                    to_log("No platform number detected in the text")
            
        return denoised_audio, framerate

async def main():
    # Your main function logic goes here
    audio_files = os.listdir(audio_folder_path)
    if audio_files:  # Check if there are any files
        file = audio_files[0]
        if file.endswith('.wav'):  # Make sure we're reading a WAV file
            file_path = os.path.join(audio_folder_path, file)
            try:
                audio_data, sample_rate = to_text(file_path)
                to_log(f"Successfully processed WAV file: {file}")
                
            except Exception as e:
                to_log(f"Error processing WAV file: {e}")

async def run_periodically():
    while True:
        await main()
        await asyncio.sleep(5)  # Wait for 5 seconds before next execution

if __name__ == "__main__":
    asyncio.run(run_periodically())



