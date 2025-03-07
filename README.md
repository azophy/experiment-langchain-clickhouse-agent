Experiment With LLM
===================

My learning on technology around LLM

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
2. edit .env.example into .env & edit accordingly
3. run `docker compose up -d`
4. visit `localhost:3000`
