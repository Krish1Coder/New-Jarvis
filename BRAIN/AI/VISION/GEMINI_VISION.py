import os
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai

# Configure Gemini API
api_key = os.environ["GEMINI"]
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

def save_image(data_url, filename='GARBAGE/captured_image.jpg'):
    try:
        header, encoded = data_url.split(",", 1)
        data = base64.b64decode(encoded)
        image = Image.open(BytesIO(data))
        image.save(filename)
    except Exception as e:
        print(f"Error saving image: {e}")
        raise

def upload_image_and_get_response(query):
    try:
        sample_file = genai.upload_file(path="GARBAGE/captured_image.png", display_name="captured_image")
        response = model.generate_content([sample_file, query])
        return response.text
    except Exception as e:
        print(f"Error processing image: {e}")
        return "An error occurred while processing the image."

# Example usage
if __name__ == "__main__":
    response = upload_image_and_get_response("What is this")
    print("Gemini Response:", response)
