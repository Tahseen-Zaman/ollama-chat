import uuid
from typing import Dict, List
from models import ChatMessageV2, Message

session_store: Dict[str, List[Message]] = {}

def create_session() -> str:
    session_id = str(uuid.uuid4())
    session_store[session_id] = []
    return session_id

def get_session(session_id: str) -> List[Message]:
    return session_store.get(session_id, [])

def append_message(session_id: str, role: str, content: str):
    if session_id in session_store:
        session_store[session_id].append(ChatMessageV2(role=role, content=content))

def end_session(session_id: str):
    session_store.pop(session_id, None)
