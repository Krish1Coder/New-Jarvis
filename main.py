from flask import Flask, render_template, request, jsonify

from ENGINE.TTS import speak

app = Flask(__name__, template_folder='GUI', static_folder='GUI/static')

@app.route('/')
def index():
    #speak("Good Morning, Sir")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    