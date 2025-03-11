Experiment With LLM
===================

My learning on technology around LLM

## Components
- main.py : main webserver files a.k.a the http handler/controller
- llm.py : contains all LLM-related code, including all LangGraph agent setup
- clickhouse.py : contains Clickhouse connection setup, provide basic tools to be consumed by llm.py as LLM Agent tool

## progress on 2025-03-10

![ClickhouseBot Screenshot](misc/screenshot-clickhouse.png?raw=true "ClickhouseBot Screenshot")

- created basic Clickhouse query LLM Agent
- using [Covid dataset from clickhouse](https://clickhouse.com/docs/getting-started/example-datasets/covid19)
- using clickhouse_connect python library for DB SDK
- using basic prompt from langhub
- should be extendable using progress from https://github.com/anandarh/faiss-sql

## progress on 2025-03-07

![Poems Bot Screenshot](misc/screenshot.png?raw=true "PoemsBot Screenshot")

- created basic chat bot for generating poems given number of lines and beginning word
- key technology:
    - Python
    - UV as package manager
    - ClickHouse as Olap database
    - LangChain as LLM Framework
    - Groq as LLM Model provider
    - FastAPI for web frameworks
    - the frontend is using vanilla javascript with Server-Sent Event for streaming response

## how to use

1. clone this repo
2. edit `.env.example` into `.env` & edit accordingly (especially the API key)
3. run `docker compose up -d`
4. visit `localhost:3000`

## Notes & learning
- official clickhouse_connect python driver only support HTTP and SQLAlchemy version < 2.x : https://clickhouse.com/docs/integrations/python#requirements-and-compatibility
- there are official tutorial from langchain for integrating SQL-based Q&A : https://python.langchain.com/docs/tutorials/sql_qa/#setup
- current dependency for langchain seems only support SQLAchemy 2.x
- there are long discussion about this topic but it seems its a dead end:
    - https://github.com/langchain-ai/langchain/issues/2454
    - https://github.com/langchain-ai/langchain/discussions/19691
- detailed API References for Langchain's SQLDatabaseToolkit: https://python.langchain.com/api_reference/community/agent_toolkits/langchain_community.agent_toolkits.sql.toolkit.SQLDatabaseToolkit.html
- there are also in-depth tutorial for building SQL agent for LangGraph. but it seems its tightly couple with langgraph: https://langchain-ai.github.io/langgraph/tutorials/sql-agent/#define-the-workflow
- coba [setup SQLDatabase langchain](https://python.langchain.com/docs/tutorials/sql_qa/#sample-data) pakai package https://github.com/cloudflare/sqlalchemy-clickhouse dapat error terkait import di dalamnya
