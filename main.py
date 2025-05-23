from fastapi import FastAPI, HTTPException
from models import (
    ChatResponse,
    ChatWithPackagesResponse,
    SingleTurnRequest,
    SingleTurnRequestV2,
)
from chat import single_turn_chat, single_turn_chat_tools
from session_manager import create_session, get_session, append_message, end_session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = "llama3.2"  # default model


@app.get("/")
def root():
    return {"message": "Welcome to the Saira!"}


@app.get("/chat/new")
def start_chat():
    session_id = create_session()
    return {"session_id": session_id}


class ChatInput(BaseModel):
    message: str


class SingleChatInput(BaseModel):
    message: list[str]


# @app.post("/chat/{session_id}", response_model=ChatResponse)
# def continue_chat(session_id: str, user_input: ChatInput):
#     history = get_session(session_id)
#     if history is None:
#         raise HTTPException(status_code=404, detail="Session not found")

#     # Add user's message
#     append_message(session_id, "user", user_input.message)

#     # Call Ollama
#     reply = multi_turn_chat(ChatRequest(model=MODEL, messages=history))

#     # Add assistant's reply to history
#     append_message(session_id, "assistant", reply)

#     return {"response": reply}


@app.post("/planning-tours/{session_id}", response_model=ChatWithPackagesResponse)
async def single_chat_planning(user_input: ChatInput, session_id: str):
    history = get_session(session_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Session not found")

    append_message(session_id, "user", user_input.message)
    if history == []:
        raise HTTPException(status_code=400, detail="No messages in session")
    request = SingleTurnRequestV2(model=MODEL, prompt=history)
    reply, packages = await single_turn_chat_tools(request)
    append_message(session_id, "assistant", reply)

    return ChatWithPackagesResponse(response=reply, packages=packages)


@app.delete("/chat/end/{session_id}")
def end_chat(session_id: str):
    end_session(session_id)
    return {"message": f"Session {session_id} ended"}


@app.post("/single", response_model=ChatResponse)
def single_chat(user_input: SingleChatInput):
    request = SingleTurnRequest(model=MODEL, prompt=user_input.message)
    reply = single_turn_chat(request)
    return {"response": reply}
