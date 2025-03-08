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

