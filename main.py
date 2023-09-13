import enum
from datetime import datetime

import fastapi.exceptions
import pydantic
from fastapi import FastAPI, WebSocket, HTTPException
import uuid


app = FastAPI()


# class CreateTransaction(pydantic.BaseModel):
#     amount: float
#     timestamp: datetime
#     description: str
#     category: str
#
#
# class Transaction(CreateTransaction):
#     id: str
#
#
# storage: dict[str, Transaction] = {}
#
#
# @app.post("/transactions/")
# async def create_transaction(transaction_data: CreateTransaction) -> Transaction:
#     transaction_id = uuid.uuid4()
#     transaction = Transaction(id=str(transaction_id), **transaction_data.model_dump())
#     storage[str(transaction_id)] = transaction
#     return transaction
#
#
# @app.get("/transactions/")
# async def get_transactions() -> list[Transaction]:
#     return list(storage.values())
#
#
# @app.get("/transactions/{transaction_id}")
# async def get_transactions(transaction_id: str) -> Transaction:
#     transaction = storage.get(transaction_id)
#     if transaction is None:
#         raise fastapi.exceptions.HTTPException(
#             status_code=fastapi.status.HTTP_404_NOT_FOUND,
#             detail=f"Transaction with id{transaction_id=} not found",
#         )
#     return transaction
#
#
# @app.delete("/transactions/{transaction_id}")
# async def delete_transactions(transaction_id: str) -> None:
#     transaction = storage.pop(transaction_id, None)
#     if transaction is None:
#         raise fastapi.exceptions.HTTPException(
#             status_code=fastapi.status.HTTP_404_NOT_FOUND,
#             detail=f"Transaction with id{transaction_id=} not found",
#         )
#
#
# @app.put("/transactions/{transaction_id}")
# async def update_transactions(
#     transaction_id: str, transaction_data: CreateTransaction
# ) -> Transaction:
#     transaction = storage.pop(transaction_id, None)
#     if transaction is None:
#         raise fastapi.exceptions.HTTPException(
#             status_code=fastapi.status.HTTP_404_NOT_FOUND,
#             detail=f"Transaction with id{transaction_id=} not found",
#         )
#     updated_transactions = Transaction(
#         id=transaction_id, **transaction_data.model_dump()
#     )
#     storage[transaction_id] = updated_transactions
#     return updated_transactions


# class MassageStatus(enum.Enum):
#     DELIVERED = "delivered"
#     READ = "read"


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
async def get_messages(chat_id: str | None = None):
    return (
        messages
        if chat_id is None
        else [message for message in messages if message.chat_id == chat_id]
    )
# @app.post("/transactions/")
# async def create_transaction(transaction_data: CreateTransaction) -> Transaction:
#     transaction_id = uuid.uuid4()
#     transaction = Transaction(id=str(transaction_id), **transaction_data.model_dump())
#     storage[str(transaction_id)] = transaction
#     return transaction