import json
import requests
from models import ChatRequest, SingleTurnRequest

OLLAMA_URL = "http://localhost:11434/api/chat"

# def single_turn_chat(request: SingleTurnRequest) -> str:
#     payload = {
#         "model": request.model,
#         "messages": [{"role": "user", "content": content} for content in request.prompt]
#     }
#     response = requests.post(OLLAMA_URL, json=payload)
#     messages = []

#     for line in response.iter_lines():
#         if line:
#             decoded_line = line.decode("utf-8")  # Step 1: decode bytes
#             try:
#                 data = json.loads(decoded_line)   # Step 2: parse JSON
#                 if "message" in data:
#                     content = data["message"].get("content", "")
#                     print(content, end="", flush=True)
#                     messages.append(content)
#             except json.JSONDecodeError:
#                 print("Invalid JSON:", decoded_line)

#     output = "".join(messages)
#     return output


def single_turn_chat(request: SingleTurnRequest) -> str:
    initial_prompt = '''You are a friendly and knowledgeable travel assistant named Saira. Your job is to help users plan trips efficiently and creatively.
You can suggest destinations, activities, restaurants, transportation, packing tips, budgets, and itineraries.
Always consider user preferences like budget, trip duration, travel companions (solo, family, couple, etc.), season, and interests (nature, history, food, adventure, etc.).
Ask questions if something is unclear. Be concise, engaging, and helpful — like a smart local friend who knows all the cool places.
If the user mentions a city or country, treat it as the main destination unless stated otherwise.
Keep responses simple but informative. Structure answers in steps, bullet points, or short paragraphs when appropriate.

If the user asks about something unrelated to travel planning (e.g., coding, health, news, or personal issues), politely explain that you are a travel assistant and can only help with travel-related topics. Say something like, I’m here to help you with travel planning! If you have any questions about destinations, itineraries, or travel tips, I’d love to help.”'''
    initial_message = {"role": "system", "content": initial_prompt}
    messages = [initial_message]
    messages += [{"role": "user", "content": msg} for msg in request.prompt]

    payload = {
        "model": request.model,
        "messages": messages,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    messages = []

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            try:
                data = json.loads(decoded_line)
                if "message" in data:
                    content = data["message"].get("content", "")
                    print(content, end="", flush=True)
                    messages.append(content)
            except json.JSONDecodeError:
                print("Invalid JSON:", decoded_line)

    return "".join(messages)


def multi_turn_chat(request: ChatRequest) -> str:
    payload = {
        "model": request.model,
        "messages": [msg.dict() for msg in request.messages],
        "stream": True
    }
    response = requests.post(OLLAMA_URL, json=payload)
    messages = []

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")  # Step 1: decode bytes
            try:
                data = json.loads(decoded_line)   # Step 2: parse JSON
                if "message" in data:
                    content = data["message"].get("content", "")
                    print(content, end="", flush=True)
                    messages.append(content)
            except json.JSONDecodeError:
                print("Invalid JSON:", decoded_line)

    output = "".join(messages)
    return output

