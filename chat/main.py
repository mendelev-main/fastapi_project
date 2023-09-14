import contextlib
from typing import AsyncIterator

import fastapi
import sqlalchemy.ext.asyncio

from . import config, models, repository, schemas


@contextlib.asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> AsyncIterator[None]:
    # on startup
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # on shutdown


app = fastapi.FastAPI(lifespan=lifespan)

engine = sqlalchemy.ext.asyncio.create_async_engine(config.POSTGRES_URL, echo=True)

create_session = sqlalchemy.ext.asyncio.async_sessionmaker(
    engine, expire_on_commit=False
)


@app.post("/messages/")
async def send_message(message_data: schemas.SendMessage) -> schemas.Message:
    async with create_session() as session:
        message_repo = repository.MessageRepo(session)
        message_model = await message_repo.insert_message(message_data)
    return schemas.Message(
        timestamp=message_model.timestamp,
        edited=message_model.edited,
        status=message_model.status,
        author_id=message_model.author_id,
        text=message_model.text,
        chat_id=message_model.chat_id,
    )


# @app.get("/messages/")
# async def get_messages(chat_id: str | None = None) -> list[schemas.Message]:
#     return (
#         messages
#         if chat_id is None
#         else [message for message in messages if message.chat_id == chat_id]
#     )
