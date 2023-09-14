from datetime import datetime

import sqlalchemy.ext.asyncio
import sqlalchemy.orm


class Base(sqlalchemy.ext.asyncio.AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    author_id: sqlalchemy.orm.Mapped[str]
    chat_id: sqlalchemy.orm.Mapped[str]
    text: sqlalchemy.orm.Mapped[str]
    timestamp: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(
        server_default=sqlalchemy.func.now()
    )
    edited: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column(
        server_default=sqlalchemy.false()
    )
    status: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        default="delivered"
    )
