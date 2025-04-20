from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]

class SingleTurnRequest(BaseModel):
    model: str
    prompt: list [str]

class ChatResponse(BaseModel):
    response: str
