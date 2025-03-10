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

def create_poem_single(line_number: int, word: str):
    prompt = prompt_template.invoke({"line_number": line_number, "text": word})

    #for token in model.stream(prompt):
    #    print(token.content, end="|")

    return model.invoke(prompt) 

def create_poem_stream(line_number: int, word: str):
    prompt = prompt_template.invoke({"line_number": line_number, "text": word})

    for token in model.stream(prompt):
        #yield f"event: newtext\ndata: {token.content}\n\n"
        yield token.content
        sleep(1)

#model.invoke(messages)

#for token in model.stream(messages):
#    print(token.content, end="|")

from langchain_core.prompts import ChatPromptTemplate

system_template = "please create a poem consiting {line_number} lines that started with this word"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

from langchain import hub

sql_prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
sql_system_message = sql_prompt_template.format(dialect="Clickhouse", top_k=5)

# initialize agent
from langgraph.prebuilt import create_react_agent
from .clickhouse import list_tables, get_table_schema, db_query_tool

tools = [ list_tables, get_table_schema, db_query_tool ]
agent_executor = create_react_agent(model, tools, prompt=sql_system_message)

def query_llm_clickhouse(question):
    for step in agent_executor.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        yield step["messages"][-1].pretty_repr()

if __name__ == '__main__':
    question = "Please list total new confirmed case for each month"

    for ans in query_llm_clickhouse(question):
        print(ans)
