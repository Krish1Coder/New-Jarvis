import os
import base64
from io import BytesIO
from PIL import Image
import requests
import json

def save_image(data_url, filename='GARBAGE/captured_image.png'):
    try:
        header, encoded = data_url.split(",", 1)
        data = base64.b64decode(encoded)
        image = Image.open(BytesIO(data))
        image.save(filename)
    except Exception as e:
        print(f"Error saving image: {e}")
        raise

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def brain(encoded_image, user_query):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"

    headers = {
        "accept": "text/event-stream",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "x-deepinfra-source": "model-embed"
    }

    payload = {
        "model": "llava-hf/llava-1.5-7b-hf",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": user_query
                    }
                ]
            }
        ]
    }

    payload_json = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload_json)

    if response.status_code == 200:
        response_str = response.content.decode('utf-8')
        data = json.loads(response_str)
        answer = data['choices'][0]['message']['content']
        return answer
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

def upload_image_and_get_response(query):
    try:
        image_path = "GARBAGE/captured_image.png"
        encoded_image = encode_image_to_base64(image_path)
        response = brain(encoded_image, query)
        return response
    except Exception as e:
        print(f"Error processing image: {e}")
        return "An error occurred while processing the image."

# Example usage
if __name__ == "__main__":
    response = upload_image_and_get_response("What is this")
    print("Response:", response)
