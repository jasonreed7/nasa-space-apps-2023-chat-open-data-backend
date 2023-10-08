from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models.dataset import Dataset
from db.setup import SessionLocal, get_db


def searchDatasetsByEmbedding(db: Session, embedding: List[float]) -> Dataset:
    result = db.scalars(select(Dataset).order_by(
        Dataset.embedding.l2_distance(embedding)).limit(1))
    return result.first()
