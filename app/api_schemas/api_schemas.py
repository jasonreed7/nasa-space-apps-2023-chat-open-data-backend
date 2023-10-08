from pydantic import BaseModel


class ChatApiRequest(BaseModel):
    message: str


class DatasetApiSchema(BaseModel):
    id: int
    title: str
    description: str
    sampleData: str
