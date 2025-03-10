# start webserver
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    StreamingResponse,
)
from pydantic import BaseModel
from asyncio import sleep
from .llm import create_poem_single, create_poem_stream, query_llm_clickhouse

class PoemChat(BaseModel):
    text: str
    line_number: float

class DbQueryChat(BaseModel):
    query: str

app = FastAPI()

@app.post("/poems")
async def chat(chat: PoemChat):
    return {"result": create_poem_single(chat.line_number, chat.text) }

@app.post("/poems_stream")
async def chat(chat: PoemChat):
    return StreamingResponse(create_poem_stream(chat.line_number, chat.text), media_type="text/event-stream")

@app.post("/query_clickhouse")
async def chat(chat: DbQueryChat):
    return StreamingResponse(query_llm_clickhouse(chat.query), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="static",html = True), name="static")
