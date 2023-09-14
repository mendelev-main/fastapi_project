from datetime import datetime

import pydantic


class SendMessage(pydantic.BaseModel):
    author_id: str
    text: str
    chat_id: str


class Message(SendMessage):
    timestamp: datetime
    edited: bool = False
    status: str = "delivered"
