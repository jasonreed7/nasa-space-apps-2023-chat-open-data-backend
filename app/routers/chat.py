
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api_schemas.api_schemas import ChatApiRequest, DatasetApiSchema
from db.queries.dataset_queries import searchDatasetsByEmbedding
from db.setup import get_db
from embedding.embedding import embed

router = APIRouter()


@router.post("/datasets/search/")
async def chat(chatRequest: ChatApiRequest, db: Session = Depends(get_db)) -> DatasetApiSchema:
    result = searchDatasetsByEmbedding(db, embed(chatRequest.message))
    return result
