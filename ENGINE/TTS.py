import requests
import base64
import os

def speak(text: str, model: str = "aura-arcas-en", filename: str = "output_audio.mp3"):
    """
    Converts text to speech using the Deepgram API and saves the audio.

    Parameters:
        text (str): The text to convert to speech.
        model (str): The voice model to use for speech generation.
                            - aura-asteria-en
                            - aura-arcas-en
                            - aura-luna-en
                            - aura-zeus-en
        filename (str): The file to save the audio output.
    """
    
    os.makedirs("GARBAGE", exist_ok=True)

    filepath = os.path.join("GARBAGE", filename)
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

    url = "https://deepgram.com/api/ttsAudioGeneration"
    payload = {"text": text, "model": model}

    response = requests.post(url, json=payload)
    response.raise_for_status() 

    with open(filepath, 'wb') as audio_file:
        audio_file.write(base64.b64decode(response.json()['data']))

if __name__ == "__main__":
    speak("Hello I am Jarvis, your personal AI Assistant, what can I do for you today, sir", filename="tts.mp3")
