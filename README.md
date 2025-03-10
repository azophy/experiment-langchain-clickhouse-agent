Experiment With LLM
===================

My learning on technology around LLM

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

### how to use

1. clone this repo
2. edit `.env.example` into `.env` & edit accordingly (especially the API key)
3. run `docker compose up -d`
4. visit `localhost:3000`
