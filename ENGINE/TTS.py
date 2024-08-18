import requests
import base64
import os
import time
import logging

def speak(text: str, voice_name: str = "mrbeast"):
    """
    Converts text to speech using the Speechify API and saves the audio.

    Parameters:
        text (str): The text to convert to speech.
        voice_name (str): The voice model to use for speech generation.
                          Available voices:
                          - jamie
                          - mrbeast
                          - snoop
                          - henry
                          - gwyneth
                          - cliff
                          - narrator
    """
    os.makedirs("GARBAGE", exist_ok=True)

    # Use a timestamp to ensure the filename is unique
    timestamp = str(int(time.time()))
    filename = f"output_audio_{timestamp}.mp3"
    filepath = os.path.join("GARBAGE", filename)

    url = "https://audio.api.speechify.com/generateAudioFiles"
    payload = {
        "audioFormat": "mp3",
        "paragraphChunks": [text],
        "voiceParams": {
            "name": voice_name,
            "engine": "speechify",
            "languageCode": "en-US"
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return None

    try:
        audio_data = base64.b64decode(response.json()['audioStream'])
    except KeyError:
        logging.error("Key 'audioStream' not found in the response")
        return None

    with open(filepath, 'wb') as audio_file:
        audio_file.write(audio_data)

    print(f"Audio saved at: {filepath}")
    return filename

if __name__ == "__main__":
    text = "Namaste sir, mai bhadiya hu aap kaise ho?"
    speak(text)
    