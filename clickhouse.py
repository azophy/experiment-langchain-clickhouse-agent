import os
from dotenv import load_dotenv

load_dotenv()

CLICKHOUSE_HOST=os.getenv('CLICKHOUSE_HOST')
CLICKHOUSE_USER=os.getenv('CLICKHOUSE_USER')
CLICKHOUSE_PASSWORD=os.getenv('CLICKHOUSE_PASSWORD')
CLICKHOUSE_DB=os.getenv('CLICKHOUSE_DB')
# connect to clickhouse using official clickhouse_connect package
import clickhouse_connect

def get_client():
    return clickhouse_connect.get_client(host=CLICKHOUSE_HOST, username=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)

from langchain_core.tools import tool

def join_query_row(result, separator='|'):
    return separator.join(map(str, result))

def join_query_results(result, col_separator='|', row_separator="\n"):
    return row_separator.join([
        join_query_row(row) for row in result
    ])

# lanchain tools based on tutorial in: https://langchain-ai.github.io/langgraph/tutorials/sql-agent/#define-tools-for-the-agent
@tool
def list_tables() -> str:
    """
    Get list of available tables inside database
    """
    client = get_client()
    res = client.query('SHOW tables');
    return join_query_row(res.result_rows[0])

@tool
def get_table_schema(table_name: str) -> str:
    """
    Retrieve SQL schema of the provide table_name
    """
    client = get_client()
    # get create query
    res = client.query(f"SHOW CREATE TABLE {table_name}");
    final_res = join_query_results(res.result_rows)

    # get 3 sample rows
    res = client.query(f"SELECT * FROM {table_name} LIMIT 3");
    final_res += f"\n\n/*\n 3 rows from table {table_name}\n" 
    final_res += join_query_row(res.column_names) + "\n"
    final_res += join_query_results(res.result_rows) + "\n*/"

    return final_res

@tool
def db_query_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    client = get_client()
    result = client.query(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return join_query_results(result.result_rows)

if __name__ == '__main__':
    print(list_tables.invoke(''))
    print(get_table_schema.invoke('covid19'))
    print(db_query_tool.invoke("SELECT formatReadableQuantity(count()) FROM covid19"))
