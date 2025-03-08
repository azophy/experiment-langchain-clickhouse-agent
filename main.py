import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("llama3-8b-8192", model_provider="groq")

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage("please create a poem consiting 8 lines that started with this word"),
    HumanMessage("Cat"),
]

#model.invoke(messages)

#for token in model.stream(messages):
#    print(token.content, end="|")

from langchain_core.prompts import ChatPromptTemplate

system_template = "please create a poem consiting {line_number} lines that started with this word"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

# connect to clickhouse
import clickhouse_connect

client = clickhouse_connect.get_client(host=os.getenv('CLICKHOUSE_HOST'), username=os.getenv('CLICKHOUSE_USER'), password=os.getenv('CLICKHOUSE_PASSWORD'))

# start webserver
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    StreamingResponse,
)
from pydantic import BaseModel
from asyncio import sleep

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
