import requests
import json
import os
from groq import Groq

# Global variable for chat history
chat_history = []

def append_history(user_query: str, res: str, query_type: str):
    """
    Appends the user's query, its classification, and the AI's response to the chat history.
    """
    global chat_history
    chat_history.append({"role": "user", "content": f"{query_type}: {user_query}"})
    chat_history.append({"role": "assistant", "content": res})

def get_web_info(query, max_results=4, prints=False) -> str:
    """
    Retrieves real-time web search results for a given query.
    """
    print(query)
    try:
        url = f"https://oevortex-webscout-api.hf.space/api/search-and-extract?q={query}&max_results={max_results}&safesearch=moderate&region=wt-wt&backend=html&max_chars=2000&extract_only=true"
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        results = response.json()

        processed_results = [{
            "link": item.get("link", ""),
            "text": item.get("text", "")
        } for item in results]

    except requests.RequestException as e:
        if prints: print(f"Error fetching web info: {e}")
        return json.dumps({"error": "Failed to retrieve web info"})

    return json.dumps(processed_results)

def determine_query_type(query, system_prompt="Your name is Jarvis\nDetermine if the query is real-time or general. If you don't know the answer, respond with 'real-time'. For example, 'hii, how are you, okay, what should I ask you before this, rock, paper, scissors, tell me the score, who is elon musk...' is general because you know the answer of it and 'who won this IPL, who is the present prime minister of India?, Jarvis tell me the news, tell me this song lyrics...' is real-time so you cannot answer these questions thats why it's real-time. Only respond with 'real-time' or 'general' and if the query is automation like 'open youtube, search in google for Elon Musk....' response 'automation', or if the query is someting which have to use vision like 'what is in my hand, see the camera and tell me what is this, jarvis is this diet coke have calarories, what is this, jarvid dekho mai kaisa lag rha hu....' response vision, and if the query is 'do you have real time data', or something related to asking about do you have real time data then you should marks it as general, and please don't write any other text you are work is to only classify the query you are not a talking AI your work is to only the classify the query, I have making response from another API so you don't have to answer it, and if the query is reated to asking date or time classify it as general, if query said to search in internet then classify real-time, and if the query is related to weather then it is general.", prints=False) -> str:
    """
    Determines if the query is real-time or general using the Groq API.
    """
    messages = [{
        "role": "system",
        "content": system_prompt
    }, {
        "role": "user",
        "content": query
    }]

    api_key = os.environ["GROQ_AI"]

    response = Groq(api_key=api_key).chat.completions.create(
        model='llama3-70b-8192', messages=messages, max_tokens=50)

    response_message = response.choices[0].message.content.strip()
    print(response_message)
    if prints: print(f"Query Type Response: {response_message}")

    return response_message.lower()

def generate(user_prompt, system_prompt="Be short and concise.", prints=False, conversation_history=None) -> str:
    """
    Generates a response to the user's prompt using Groq or real-time data from Oevortex.
    """
    if conversation_history is None:
        conversation_history = []

    # Determine if the query is real-time or general
    query_type = determine_query_type(user_prompt)

    if query_type == "real-time":
        # Fetch real-time data
        web_info = get_web_info(user_prompt, prints=prints)

        # Process the results to extract relevant text
        search_results = json.loads(web_info)
        search_texts = " ".join(item['text'] for item in search_results if item['text'])

        # Send the search results to Groq for final response
        messages = conversation_history + [{
            "role": "system",
            "content": system_prompt
        }, {
            "role": "user",
            "content": user_prompt
        }, {
            "role": "user",
            "content": f"Search results: {search_texts}"
        }]

        api_key = os.environ["GROQ_AI"]

        response = Groq(api_key=api_key).chat.completions.create(
            model='llama3-70b-8192', messages=messages, max_tokens=4000)

        response_message = response.choices[0].message.content
        print(response_message)

    else:
        # Proceed with general response using Groq
        function_descriptions = {
            "type": "function",
            "function": {
                "name": "get_web_info",
                "description": "Gets real-time information about the query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search on the web. And today is 2024, and you have to search from India and in 2024...",
                        },
                    },
                    "required": ["query"],
                },
            },
        }

        messages = conversation_history + [{
            "role": "system",
            "content": system_prompt
        }, {
            "role": "user",
            "content": user_prompt
        }]

        api_key = os.environ["GROQ_AI"]

        response = Groq(api_key=api_key).chat.completions.create(
            model='llama3-70b-8192',
            messages=messages,
            tools=[function_descriptions],
            tool_choice="auto",
            max_tokens=2000)

        response_message = response.choices[0].message.content
        print(response_message)

    # Append to conversation history using the new function
    append_history(user_prompt, response_message, query_type)

    return response_message, conversation_history

def generate_groq(user_prompt, system_prompt, prints=False, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    # Add the system prompt and user prompt to the messages
    messages = conversation_history + [{
        "role": "system",
        "content": system_prompt
    }, {
        "role": "user",
        "content": user_prompt
    }]

    api_key = os.environ["GROQ_AI"]

    response = Groq(api_key=api_key).chat.completions.create(
        model='llama3-70b-8192', messages=messages, max_tokens=4000)

    response_message = response.choices[0].message.content

    # Print the response message if needed
    print(response_message)

    # Append to conversation history using the new function
    query_type = determine_query_type(user_prompt)
    append_history(user_prompt, response_message, query_type)

    return response_message, conversation_history

def main():
    conversation_history = []
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        response, conversation_history = generate(
            user_prompt=user_prompt,
            conversation_history=conversation_history,
            prints=True)
        print("AI:", response)

if __name__ == "__main__":
    main()
