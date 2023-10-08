from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from db.setup import Base, engine


class Dataset(Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text, unique=True)
    description: Mapped[str] = mapped_column(Text)
    sampleData: Mapped[str] = mapped_column(Text)
    embedding: Mapped[List[float]] = mapped_column(Vector(384))


Base.metadata.create_all(engine)
