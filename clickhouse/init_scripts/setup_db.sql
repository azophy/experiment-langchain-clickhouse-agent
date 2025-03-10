-- preparing example dataset: https://clickhouse.com/docs/getting-started/example-datasets/covid19
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
    LIMIT 100000 -- use this to limit the dataset
    ;

