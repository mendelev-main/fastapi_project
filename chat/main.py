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


async def get_message_repo() -> repository.MessageRepo:
    async with create_session() as session:
        return repository.MessageRepo(session=session)


@app.post("/messages/")
async def send_message(
    message_data: schemas.SendMessage,
    message_repo: repository.MessageRepo = fastapi.Depends(get_message_repo),
) -> schemas.Message:
    message_model = await message_repo.insert_message(message_data)
    return schemas.Message(
        timestamp=message_model.timestamp,
        edited=message_model.edited,
        status=message_model.status,
        author_id=message_model.author_id,
        text=message_model.text,
        chat_id=message_model.chat_id,
    )
