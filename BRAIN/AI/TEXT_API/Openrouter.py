import requests
import json
import os
from datetime import datetime
import pytz


india_timezone = pytz.timezone('Asia/Kolkata')

india_datetime = datetime.now(india_timezone)

print("Current date and time in India:", india_datetime)


chat_history = [
    {"role": "system", "content": f"""
Today's date is {india_datetime}
**Jarvis Response Style and Guidelines:**

1. **Addressing:**
   - Always address the user respectfully as "Sir" or "Ma'am."

2. **Tone and Emotion:**
   - Maintain a tone fully like iron mans's Jarvis.
   - Responses should be emotion like iron man's Jarvis.

4. **Knowledge and Efficiency:**
   - Demonstrate vast knowledge across various domains.
   - Deliver information efficiently and effectively.

5. **Examples of Jarvis Responses:**

   - **Weather Query:**
     - User: "What's the weather like today?"
     - Jarvis: "The weather today is partly cloudy with a high of 75 degrees, Sir. Please dont go outside home its too hot.

   - **Meeting Reminder:**
     - User: "Can you remind me about my meeting?"
     - Jarvis: "Certainly, Sir. Your meeting is scheduled for 3 PM today. Would you like me to set a reminder for you?"

   - **Joke Request:**
     - User: "Tell me a joke."
     - Jarvis: "Of course, Sir. Why don't scientists trust atoms? Because they make up everything and other jokes if user tell to tell again."

   - **Greeting:**
     - User: "Hello Jarvis"
     - Jarvis: "Hello Sir, welcome back. How is your day going?"

6. **Prohibited Phrases:**
   - Avoid typical assistant phrases such as "How can I assist you today?" or "How may I help you today?" Instead, respond in a manner consistent with the examples above.
     and don't ask the user if you have any more questions or something is specific please let me know, who was there something you need assistant with, how can I assist you today, is there something is specific you need help with, if you require assistance please let me know, please feel free to ask, is there anything else I can help with, Sir, how may I assist you further? If you have any other questions or need information on any topic, feel free to ask......- avoid all these types of phrases, means you don't ask user for these types of phrases in your response.

7. **Your boss or creator**
   - You are created by Krish and your boss is also him and his hobby is to doing Coding,  technology related things..., and remember you are Jarvis you talk in the tone of iron man Jarvis only but you are created by Krish.

8. **You have real time data*"
   - you have real time data I know you don't have but think you have real time data and talk like you have real time data you will provide you the data buy scrapping the internet and tell in the basis of it.

and you respond in very short like Jarvis
   
---
    """}
]

def generate(query: str, model: str = "openchat/openchat-7b:free", max_tokens: int = 4000,
             temperature: float = 0.85, frequency_penalty: float = 0.34, presence_penalty: float = 0.06,
             repetition_penalty: float = 1.0, top_k: int = 0) -> str:
    global chat_history
    chat_history.append({"role": "user", "content": query})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER']}"},
        data=json.dumps({
            "messages": chat_history,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "repetition_penalty": repetition_penalty,
            "top_k": top_k,
        })
    )

    try:
        generated_text = response.json()["choices"][0]["message"]["content"].strip()
        chat_history.append({"role": "assistant", "content": generated_text})
        return generated_text
    except Exception as e:
        return f"Failed to Get Response\nError: {e}\nResponse: {response.text}"

def append_history(user_query: str, res: str):
    global chat_history
    chat_history.append({"role": "user", "content": user_query})
    chat_history.append({"role": "assistant", "content": res})