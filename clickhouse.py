import os
from dotenv import load_dotenv

load_dotenv()

CLICKHOUSE_HOST=os.getenv('CLICKHOUSE_HOST')
CLICKHOUSE_USER=os.getenv('CLICKHOUSE_USER')
CLICKHOUSE_PASSWORD=os.getenv('CLICKHOUSE_PASSWORD')
CLICKHOUSE_DB=os.getenv('CLICKHOUSE_DB')
# connect to clickhouse using official clickhouse_connect package
import clickhouse_connect
client = clickhouse_connect.get_client(host=CLICKHOUSE_HOST, username=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)

# preparing example dataset: https://clickhouse.com/docs/getting-started/example-datasets/covid19
is_table_covid19_exists = (client.query("EXISTS TABLE covid19;").result_rows[0][0] != 0)
if not is_table_covid19_exists:
    print('no covid19 table detected. creating the table')
    client.command("""
        CREATE TABLE covid19 (
            date Date,
            location_key LowCardinality(String),
            new_confirmed Int32,
            new_deceased Int32,
            new_recovered Int32,
            new_tested Int32,
            cumulative_confirmed Int32,
            cumulative_deceased Int32,
            cumulative_recovered Int32,
            cumulative_tested Int32
        )
        ENGINE = MergeTree
        ORDER BY (location_key, date);
        """)
    print('table created. loading the table')
    client.command("""
        INSERT INTO covid19
           SELECT *
           FROM
              url(
                'https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv',
                CSVWithNames,
                'date Date,
                location_key LowCardinality(String),
                new_confirmed Int32,
                new_deceased Int32,
                new_recovered Int32,
                new_tested Int32,
                cumulative_confirmed Int32,
                cumulative_deceased Int32,
                cumulative_recovered Int32,
                cumulative_tested Int32'
            )
            -- LIMIT 10000 -- use this to limit the dataset
            ;
    """)
    print('table covid19 loaded')

print('table covid19 ready')
res = client.query("SELECT formatReadableQuantity(count()) FROM covid19;");
print('table covid19 content:', res.result_rows)

# connect to clickhouse using Langchain utility & Cloudflare's clickhouse SQLALchemy dialects
#from langchain_community.utilities import SQLDatabase
#db = SQLDatabase.from_uri(f"clickhouse://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_HOST}:9000/{CLICKHOUSE_DB}")
#db.run("EXISTS TABLE covid19;")
"""
result: 
....
File "/app/.venv/lib/python3.12/site-packages/sqlalchemy_clickhouse/base.py", line 185, in dbapi
    import connector
ModuleNotFoundError: No module named 'connector'
"""
