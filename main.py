import os
import base64
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import pytz
from ENGINE.TTS import speak
from BRAIN.AI.TEXT_API.Openrouter import generate, append_history
from BRAIN.AI.TEXT_API.Groq import determine_query_type, get_web_info, generate_groq
from BRAIN.AI.VISION.GEMINI_VISION import upload_image_and_get_response as vision
#from BRAIN.AI.VISION.LLAVA_VISION import upload_image_and_get_response as vision

app = Flask(__name__, template_folder='GUI', static_folder='GUI/static')

india_timezone = pytz.timezone('Asia/Kolkata')

# Get the current date and time in India
india_datetime = datetime.now(india_timezone)

print("Current date and time in India:", india_datetime)


@app.route('/')
def index():
    return render_template('index.html')

def delayed_vision_response(user_input, delay):
    """
    Function to handle vision analysis with a delay.
    """
    def process_vision():
        response_text = vision(user_input)
        return response_text

    result = None
    def wrapper():
        nonlocal result
        result = process_vision()

    timer = threading.Timer(delay, wrapper)
    timer.start()
    timer.join()  # Wait for the timer to finish
    return result  # Return the result after the timer finishes

@app.route('/process_speech', methods=['POST'])
def process_speech():
    user_input = request.json.get('text')
    classification = determine_query_type(user_input)

    try:
        # Clear old audio files in the GARBAGE directory
        garbage_dir = 'GARBAGE'
        for filename in os.listdir(garbage_dir):
            file_path = os.path.join(garbage_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        if classification == "general":
            response_text = generate(user_input)
            

        elif classification == "real-time":
            
            format_data = generate_groq(f"Here is the query:\n{user_input}", system_prompt=f"Todays date is {india_datetime}, format this query it has to search on the web, today is 2024 and you have to search from India and in 2024. and if it is news then also add date to it like if user ask who win this IPL you response IPL 2024 results, Tell me the news you respose 'today 'date' news India' and you have to only resposne the formatted query not any other text you are work is to only format the query so it will perfectly search on the web and don't respond any other text also don't respond in '',sir, all other things")
            
            results = get_web_info(format_data)
            final_res = generate_groq(f"{results} \n\n\n These are search results you have to provide the answer of question given below in short\n\n{user_input}", system_prompt="Be short and concise.")
            append_history(user_input, results)
            if isinstance(final_res, tuple):
                text_result = final_res[0]  # Extract the string element
                frmt_res = text_result.replace(",[object Object],[object Object]", "")
            else:
                frmt_res = final_res.replace(".,[object Object],[object Object]", "")

            response_text = frmt_res
            append_history(user_input, frmt_res)
            speak(response_text)
            

        elif classification == "automation":
            response_text = "This is an automation"

        elif classification == "vision":
            response_text = "Analysing Sir..."
            #speak(response_text)
            return jsonify(response=response_text, audio_file="")

        else:
            response_text = "this is dont know"

        # Generate TTS
        audio_filename = speak(response_text)

        # Handle case when speak returns None
        if audio_filename is None:
            return jsonify(response=response_text, audio_file="")

        return jsonify(response=response_text, audio_file=f'/GARBAGE/{audio_filename}')

    except Exception as e:
        print(e)
        return jsonify(response="An error occurred while processing your request.", audio_file="")

@app.route('/GARBAGE/<path:filename>')
def serve_garbage_file(filename):
    return send_from_directory('GARBAGE', filename)

@app.route('/capture_image', methods=['POST'])
def capture_image():
    image_data = request.json.get('image')
    if image_data:
        image_data = image_data.split(",")[1]
        image_path = os.path.join('GARBAGE', 'captured_image.png')

        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(image_data))

        return jsonify({"status": "success", "file": image_path})
    return jsonify({"status": "error", "message": "No image data received"})

@app.route('/process_vision', methods=['POST'])
def process_vision():
    user_input = request.json.get('text')
    response_text = delayed_vision_response(user_input, delay=2)
    append_history(user_input, response_text)
    
    audio_filename = speak(response_text)

    # Handle case when speak returns None
    if audio_filename is None:
        return jsonify(response=response_text, audio_file="")

    return jsonify(response=response_text, audio_file=f'/GARBAGE/{audio_filename}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')