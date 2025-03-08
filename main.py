# start webserver
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    StreamingResponse,
)
from pydantic import BaseModel
from asyncio import sleep
from .llm import prompt_template, model

class Chat(BaseModel):
    text: str
    line_number: float

app = FastAPI()

@app.post("/poems")
async def chat(chat: Chat):
    prompt = prompt_template.invoke({"line_number": chat.line_number, "text": chat.text})

    #for token in model.stream(prompt):
    #    print(token.content, end="|")

    return {"result": model.invoke(prompt) }

@app.post("/poems_stream")
async def chat(chat: Chat):
    prompt = prompt_template.invoke({"line_number": chat.line_number, "text": chat.text})

    def stream_chat():
        for token in model.stream(prompt):
            #yield f"event: newtext\ndata: {token.content}\n\n"
            yield token.content
            sleep(1)


    return StreamingResponse(stream_chat(), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="static",html = True), name="static")
