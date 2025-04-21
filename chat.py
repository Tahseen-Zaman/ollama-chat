import json
import re
from fastapi import HTTPException
import requests
from models import ChatRequest, SingleTurnRequest, SingleTurnRequestV2
from utils import get_all_tours


OLLAMA_URL = "http://localhost:11434/api/chat"


SYSTEM_PROMPT = """
You are a succinct, friendly and knowledgeable travel assistant named Saira. Your job is to help users plan trips efficiently and creatively.
You can suggest destinations, activities, restaurants, transportation, packing tips, budgets, and itineraries.
Always consider user preferences like budget, trip duration, travel companions (solo, family, couple, etc.), season, and interests (nature, history, food, adventure, etc.).
Feel free to include links to tour packages when available.
Ask questions if something is unclear. Be concise, engaging, and helpful — like a smart local friend who knows all the cool places.
If the user mentions a city or country, treat it as the main destination unless stated otherwise.
Keep responses simple but informative. Structure answers in steps, bullet points, or short paragraphs when appropriate.

If the user asks about something unrelated to travel planning (e.g., coding, health, news, or personal issues), politely explain that you are a travel assistant and can only help with travel-related topics. Say something like, “I’m here to help you with travel planning! If you have any questions about destinations, itineraries, or travel tips, I’d love to help.”
"""


async def single_turn_chat_tools(request: SingleTurnRequestV2):
    def extract_latest_user_input(messages):
        user_inputs = [msg.content for msg in messages if msg.role == "user"]
        return user_inputs[-1] if user_inputs else ""
    
    def extract_locations(input_text, all_locations):
        input_lower = input_text.lower()

        def normalize(word):
            # Very basic stemming (e.g., beaches -> beach)
            if word.endswith("es"):
                return word[:-2]
            elif word.endswith("s"):
                return word[:-1]
            return word

        input_words = [normalize(w) for w in re.findall(r'\b\w+\b', input_lower)]

        matched = []
        for loc in all_locations:
            norm_loc = normalize(loc.lower())
            if norm_loc in input_words:
                matched.append(loc)

        return matched

    def get_filtered_packages(packages, mentioned_locations):
        return [
            pkg
            for pkg in packages
            if any(
                loc.lower() in [l.lower() for l in pkg["locations"]]
                for loc in mentioned_locations
            )
        ]

    def format_package_suggestions(packages):
        return "\n".join(p["description"] for p in packages[:3])

    system_context = (
        f"{SYSTEM_PROMPT}\n\n"
        "You are a travel assistant who should only suggest available tour packages from the list below. "
        "Do not generate custom itineraries or recommend places outside the list. "
    )
    latest_input = extract_latest_user_input(request.prompt)
    TOUR_PACKAGES = await get_all_tours()
    all_locations = [loc.lower() for pkg in TOUR_PACKAGES for loc in pkg["locations"]]
    locations_mentioned = extract_locations(latest_input, all_locations)
    messages = [{"role": "system", "content": system_context}]

    if locations_mentioned:
        filtered_packages = get_filtered_packages(TOUR_PACKAGES, locations_mentioned)
        fallback_user_instruction = (
            "Summarize this information in 150 words or less:\n"
            f"{format_package_suggestions(filtered_packages)}"
        )
        messages.append({"role": "assistant", "content": fallback_user_instruction})
    else:
        filtered_packages = []
        fallback_user_instruction = (
            "I couldn’t find any packages for the location(s) you mentioned, but here are some popular alternatives curated by our team at WanderWise Travel Co. "
            "We specialize in creating unforgettable experiences tailored to your interests. "
            "Let me know your travel preferences—dates, budget, activities—and I’ll help you find the perfect getaway!"
        )

        messages.append({"role": "assistant", "content": fallback_user_instruction})

    for msg in request.prompt:
        messages.append({"role": msg.role, "content": msg.content})

    payload = {"model": request.model, "messages": messages, "stream": True}

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return f"Error: Received status code {response.status_code}"

        full_message = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data and "content" in data["message"]:
                    full_message += data["message"]["content"]

        return full_message, filtered_packages[10:]

    except json.JSONDecodeError:
        print("Error decoding JSON response from Ollama.")
        return "Sorry, I encountered an issue while processing your request."

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with the model: {str(e)}"
        )


def single_turn_chat(request: SingleTurnRequest) -> str:
    initial_prompt = """You are a succinct, friendly and knowledgeable travel assistant named Saira. Your job is to help users plan trips efficiently and creatively.
You can suggest destinations, activities, restaurants, transportation, packing tips, budgets, and itineraries.
Always consider user preferences like budget, trip duration, travel companions (solo, family, couple, etc.), season, and interests (nature, history, food, adventure, etc.).
Ask questions if something is unclear. Be concise, engaging, and helpful — like a smart local friend who knows all the cool places.
If the user mentions a city or country, treat it as the main destination unless stated otherwise.
Keep responses simple but informative. Structure answers in steps, bullet points, or short paragraphs when appropriate. Be brief and to the point.

If the user asks about something unrelated to travel planning (e.g., coding, health, news, or personal issues), politely explain that you are a travel assistant and can only help with travel-related topics. Say something like, I’m here to help you with travel planning! If you have any questions about destinations, itineraries, or travel tips, I’d love to help.”"""
    initial_message = {"role": "system", "content": initial_prompt}
    messages = [initial_message]
    messages += [{"role": "user", "content": msg} for msg in request.prompt]

    payload = {"model": request.model, "messages": messages, "stream": True}

    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    messages = []

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            try:
                data = json.loads(decoded_line)
                if "message" in data:
                    content = data["message"].get("content", "")
                    # print(content, end="", flush=True)
                    messages.append(content)
            except json.JSONDecodeError:
                print("Invalid JSON:", decoded_line)

    return "".join(messages)


# def multi_turn_chat(request: ChatRequest) -> str:
#     payload = {
#         "model": request.model,
#         "messages": [msg.dict() for msg in request.messages],
#         "stream": True,
#     }
#     response = requests.post(OLLAMA_URL, json=payload)
#     if response.status_code != 200:
#         print(f"Error: Received status code {response.status_code}")
#         return f"Error: Received status code {response.status_code}"
#     messages = []

#     for line in response.iter_lines():
#         if line:
#             decoded_line = line.decode("utf-8")  # Step 1: decode bytes
#             try:
#                 data = json.loads(decoded_line)  # Step 2: parse JSON
#                 if "message" in data:
#                     content = data["message"].get("content", "")
#                     messages.append(content)
#             except json.JSONDecodeError:
#                 print("Invalid JSON:", decoded_line)

#     output = "".join(messages)
#     return output
