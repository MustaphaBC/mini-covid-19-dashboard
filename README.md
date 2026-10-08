# Mini COVID-19 Dashboard

A compact COVID-19 analytics prototype with Apache Cassandra storage, a Flask JSON API, a Streamlit dashboard, and a linear-regression forecast for recent case counts by country.

## Components

- `data_preparation.py` reads the Our World in Data CSV, selects country/date/case/death fields, and inserts rows into Cassandra.
- `api/app.py` exposes country names and time-series statistics.
- `dashboard/dashboard.py` charts cases and deaths and displays a short forward forecast.
- `ml_analysis.py` fits a linear-regression model to date-based case counts.

## Requirements

- Python 3.9 or later
- A local Cassandra node at `127.0.0.1`
- `owid-covid-data.csv` in the project root (download separately; not included in the public repository)

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the database in `cqlsh`:

```sql
CREATE KEYSPACE IF NOT EXISTS covid
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE covid;

CREATE TABLE IF NOT EXISTS stats (
    country text,
    date date,
    total_cases int,
    total_deaths int,
    PRIMARY KEY ((country), date)
);
```

## Run locally

From the project root, import the data, then run the API and dashboard in separate terminals:

```bash
python data_preparation.py
```

```bash
python api/app.py
```

```bash
streamlit run dashboard/dashboard.py
```

## Implementation note

The current `data_preparation.py` imports `api.cassandra_connect`, while the connector file is at the project root as `cassandra_connect.py`. Change that import to `from cassandra_connect import connect_cassandra` before running the import step.

Datasets, database contents, and generated outputs are excluded from version control.
