import sqlalchemy.ext.asyncio

from . import models, schemas


class MessageRepo:
    def __init__(self, session: sqlalchemy.ext.asyncio.AsyncSession):
        self._session = session

    async def insert_message(self, message_data: schemas.SendMessage) -> models.Message:
        model = models.Message(**message_data.model_dump())
        self._session.add(model)
        await self._session.commit()
        return model
