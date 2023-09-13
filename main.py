from datetime import datetime

import pydantic
from fastapi import FastAPI

app = FastAPI()


class SendMessage(pydantic.BaseModel):
    author_id: str
    text: str
    chat_id: str


class Message(SendMessage):
    timestamp: datetime
    edited: bool = False
    status: str = "delivered"


messages = []


@app.post("/messages/")
async def send_message(message_data: SendMessage) -> Message:
    message = Message(
        timestamp=datetime.now(),
        edited=False,
        status="delivered",
        **message_data.model_dump()
    )
    messages.append(message)
    return message


@app.get("/messages/")
async def get_messages(chat_id: str | None = None) -> list[Message]:
    return (
        messages
        if chat_id is None
        else [message for message in messages if message.chat_id == chat_id]
    )
