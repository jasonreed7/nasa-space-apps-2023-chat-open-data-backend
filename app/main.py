from fastapi import FastAPI

from app.routers import chat as chat_router

app = FastAPI()

app.include_router(chat_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
