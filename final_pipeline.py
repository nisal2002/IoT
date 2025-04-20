import asyncio
import wave
import numpy as np
import os
import noisereduce as nr
from scipy.io import wavfile
from googletrans import Translator
import requests
import json
import speech_recognition as sr
import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
audio_folder_path = "C:\\CM3603\\esp32\\flask-server\\uploads"
class CSRNet(nn.Module):
    def __init__(self, load_weights=False):
        super(CSRNet, self).__init__()
        self.seen = 0
        self.frontend_feat = [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512]
        self.backend_feat = [512, 512, 512,256,128,64]
        self.frontend = self._make_layers(self.frontend_feat)
        self.backend = self._make_layers(self.backend_feat, in_channels=512, dilation=True)
        self.output_layer = nn.Conv2d(64, 1, kernel_size=1)

        if load_weights:
            mod = models.vgg16(pretrained=True)  # Use VGG16 without BN
            self._initialize_weights()
            self.frontend.load_state_dict(mod.features[:len(self.frontend)].state_dict())

    def forward(self, x):
        x = self.frontend(x)
        x = self.backend(x)
        x = self.output_layer(x)
        return x

    def _make_layers(self, cfg, in_channels=3, dilation=False):
        layers = []
        for v in cfg:
            if v == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                if dilation:
                    layers += [nn.Conv2d(in_channels, v, kernel_size=3, padding=2, dilation=2),
                               nn.ReLU(inplace=True)]
                else:
                    layers += [nn.Conv2d(in_channels, v, kernel_size=3, padding=1),
                               nn.ReLU(inplace=True)]
                in_channels = v
        return nn.Sequential(*layers)

    def _initialize_weights(self):
        for m in self.backend.children():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, std=0.01)
                if m.bias is not None:
                    m.bias.data.fill_(0.01)

def to_log(text):
    print(text)

def query_ollama(text):
    """
    Query Ollama API to extract platform number and time from the text
    """
    # Ollama API endpoint (default local installation)
    url = "http://localhost:11434/api/generate"
    
    # Craft the prompt
    prompt = f"""
    the following is a text of a train announcement.
    extract the platform number and train time from the text.
    return only a JSON object with 'platform' and 'time' keys.
    if information is missing, use null. the announcement might be damaged or corrupted.

    Text: {text}

    Response format:
    {{
        "platform": "number or null",
        "time": "time or null"
    }}
    """

    # Request payload
    payload = {
        "model": "deepseek-r1:1.5b",  # You can change this to any model you have pulled in Ollama
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        response_text = result.get('response', '{}')
        
        # Try to parse the JSON from the response
        try:
            info = json.loads(response_text)
            return info.get('platform'), info.get('time')
        except json.JSONDecodeError:
            to_log("Failed to parse Ollama response as JSON")
            return None, None

    except Exception as e:
        to_log(f"Error querying Ollama: {e}")
        return None, None

def trigger_camera(platform_number):
    try:
        to_log(f"Triggering camera for platform {platform_number}")
        # Add your camera triggering logic here
        return True
    except Exception as e:
        to_log(f"Error triggering camera: {e}")
        return False

def translate_sinhala_to_english(text):
    translator = Translator()
    try:
        translation = translator.translate(text, src='si', dest='en')
        return translation.text
    except Exception as e:
        to_log(f"Translation error: {e}")
        return None

def save_wav(audio_data, sample_rate, output_path):
    audio_scaled = np.int16(audio_data * 32767)
    wavfile.write(output_path, sample_rate, audio_scaled)


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
        
def check_platform_images(platform_number):
    base_path ="C:\\CM3603\\esp32\\flask-server\\platforms"
    platform_folder = os.path.join(base_path, f"platform_{platform_number}")
    if os.path.exists(platform_folder):
        images = [f for f in os.listdir(platform_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
    else:
        to_log(f"No images found for platform {platform_number}")
        return None
    to_log(f"Found {len(images)} images in platform {platform_number} folder")
    for image in images:
        total_crowd_count = 0
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = CSRNet(load_weights=True).to(device)
        model.eval()
        image_path = os.path.join(platform_folder, image)
        to_log(f"Processing image: {image_path}")
        image = Image.open(image_path).convert('RGB')
        transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225])
                            ])
        input_img = transform(image).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(input_img)
            crowd_count = torch.sum(output).item()
            total_crowd_count += crowd_count

    # Delete all processed images from the platform folder
    for image in images:
        image_path = os.path.join(platform_folder, image)
        try:
            os.remove(image_path)
            to_log(f"Deleted image: {image_path}")
        except Exception as e:
            to_log(f"Error deleting image {image_path}: {e}")

    if total_crowd_count > 100:
        return "high"
    elif total_crowd_count > 50:
        return "medium"
    else:   
        return "low"

def to_text(file_path):
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
            dtype = np.uint8
        elif sample_width == 4:
            dtype = np.int32
        
        audio_array = np.frombuffer(audio_data, dtype=dtype)
        
        # If stereo, convert to mono by averaging channels
        if n_channels == 2:
            if audio_array.size % 2 != 0:
                audio_array = audio_array[:-1]
            audio_array = audio_array.reshape(-1, 2).mean(axis=1).astype(dtype)

        # Denoise the audio
        audio_float = audio_array.astype(np.float32) 
        denoised_audio = nr.reduce_noise(y=audio_float, sr=framerate)
        
        # Save denoised audio
        file_name = os.path.splitext(file_path)[0]
        output_path = f"{file_name}_edited.wav"
        save_wav(denoised_audio, framerate, output_path)
        to_log(f"Saved denoised audio to: {output_path}")

        # Convert speech to Sinhala text
        text_result = speech_to_text(file_path, "si-LK")
        to_log(f"Sinhala text: {text_result}")
        
        # Translate and extract information
        if text_result:
            english_text = translate_sinhala_to_english(text_result)
            to_log(f"English translation: {english_text}")
            
            if english_text:
                # Extract platform number and time using Ollama
                platform_number, train_time = query_ollama(english_text)
                
                if platform_number:
                    to_log(f"Detected Platform Number: {platform_number}")
                    if trigger_camera(platform_number):
                        to_log(f"Successfully triggered camera for platform {platform_number}")
                    # Check for images in platform folder
                        count = check_platform_images(platform_number)
                        if count !=None:
                            to_log(f"Found  images in platform {platform_number} folder")
                            if count == "high":
                                to_log(f"High crowd count in train at platform {platform_number}")
                            elif count == "medium":
                                to_log(f"Medium crowd count in train at platform {platform_number}")
                            else:
                                to_log(f"Low crowd count in train at platform {platform_number}")
                        else:
                            to_log(f"No images found for platform {platform_number}")
                    else:
                        to_log(f"Failed to trigger camera for platform {platform_number}")
                else:
                    to_log("No platform number detected in the text")
                
                if train_time:
                    to_log(f"Detected Train Time: {train_time}")
                else:
                    to_log("No train time detected in the text")
            
        if not verify_audio_file(file_path):
            to_log("Invalid or corrupted audio file")
            return None, None

        return denoised_audio, framerate

def verify_audio_file(file_path):
    try:
        with wave.open(file_path, 'rb') as wav_file:
            to_log(f"Channels: {wav_file.getnchannels()}")
            to_log(f"Sample width: {wav_file.getsampwidth()}")
            to_log(f"Frame rate: {wav_file.getframerate()}")
            to_log(f"Number of frames: {wav_file.getnframes()}")
        return True
    except Exception as e:
        to_log(f"Error verifying audio file: {e}")
        return False

async def main():
    audio_files = os.listdir(audio_folder_path)
    if audio_files:
        file = audio_files[0]
        if file.endswith('.wav') or file.endswith('.mp3'):
            file_path = os.path.join(audio_folder_path, file)
            try:
                print(file_path)
                audio_data, sample_rate = to_text(file_path)
                to_log(f"Successfully processed {file}")
                
            except Exception as e:
                to_log(f"Error processing {file}: {e}")
async def run_periodically():
    while True:
        await main()
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_periodically()) 