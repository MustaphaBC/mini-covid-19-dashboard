import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify
from cassandra_connect import connect_cassandra

app = Flask(__name__)
session = connect_cassandra()

@app.route("/")
def get_countries():
    rows = session.execute("SELECT DISTINCT country FROM stats")
    countries = [row.country for row in rows]
    return jsonify(countries)

@app.route("/stats/<country>")
def get_stats(country):
    rows = session.execute("SELECT date, total_cases, total_deaths FROM stats WHERE country=%s", (country,))
    data = [
        {
            "date": str(row.date),   # conversion en string
            "total_cases": row.total_cases,
            "total_deaths": row.total_deaths
        }
        for row in rows
    ]
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
