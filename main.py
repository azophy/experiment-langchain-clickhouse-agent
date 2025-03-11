# start webserver
import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    StreamingResponse,
)
from sse_starlette.sse import EventSourceResponse
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
async def chat(chat: DbQueryChat, request: Request):
    async def generate_response():
        for event in query_llm_clickhouse(chat.query):
            # If client was closed the connection
            if await request.is_disconnected():
                break

            yield {
                "event": event.type,
                "data": json.dumps({
                    "tool": getattr(event, 'tool_calls', None),
                    "content": event.content,
                }),
            }

    return EventSourceResponse(generate_response())

app.mount("/", StaticFiles(directory="static",html = True), name="static")
