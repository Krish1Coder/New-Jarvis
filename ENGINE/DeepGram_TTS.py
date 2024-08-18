import requests
import base64
import os
import time
import logging

def speak(text: str, model: str = "aura-arcas-en"):
    """
    Converts text to speech using the Deepgram API and saves the audio.

    Parameters:
        text (str): The text to convert to speech.
        model (str): The voice model to use for speech generation.
    """
    os.makedirs("GARBAGE", exist_ok=True)

    # Use a timestamp to ensure the filename is unique
    timestamp = str(int(time.time()))
    filename = f"output_audio_{timestamp}.mp3"
    filepath = os.path.join("GARBAGE", filename)

    url = "https://deepgram.com/api/ttsAudioGeneration"
    payload = {"text": text, "model": model}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")  # HTTP error
        return None
    except Exception as err:
        logging.error(f"Other error occurred: {err}")  # Other errors
        return None

    try:
        audio_data = base64.b64decode(response.json()['data'])
    except KeyError:
        logging.error("Key 'data' not found in the response")
        return None

    with open(filepath, 'wb') as audio_file:
        audio_file.write(audio_data)

    return filename

if __name__ == "__main__":
    text = """
    Have you ever heard of the village that disappeared overnight? In 1945, the small village of Hollow Creek in England had about 50 people. One morning, a postman found the village empty. Houses were abandoned, breakfast tables were set, and even the animals were left alone.

    The authorities were called, but there were no signs of struggle or a planned move. People shared wild theories: Was it aliens? A secret government experiment? Or did they all leave for another world?

    For decades, no one knew what happened to the villagers of Hollow Creek. Then, in 1995, a hiker found an old, hidden cave near the village. Inside, he found a journal from one of the villagers.

    The journal revealed that the villagers had found underground tunnels leading to a hidden community. They moved there to escape the chaos after World War II, choosing to live in secret.

    The village of Hollow Creek didn’t really disappear; it just went underground. Follow for more intriguing stories and mysteries revealed!
    """
    speak(text)