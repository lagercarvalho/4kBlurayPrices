from flask import Flask, render_template, jsonify
import psycopg2
import json
import re
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
sale_rows = []
sale_steelbooks = []
bookable = []

def connect_db():
    with open(f'{script_dir}/../config.json', "r") as f:
        config = json.load(f)["database"]

    conn = psycopg2.connect(
        database=config["name"],
        host=config["host"],
        user=config["user"],
        password=config["password"],
        port=config["port"],
    )
    return conn

def fetch_sale(limit, offset, title_filter = None):
    conn = connect_db()
    cursor = conn.cursor()

    filter_clause = ""

    if title_filter:
        filter_clause = f"AND LOWER(title) like '%{title_filter}%'"

    sales_query = f"""
        SELECT * FROM movies
        WHERE sale != 0
        {filter_clause}
        ORDER BY sale DESC, current_price ASC, title
        LIMIT {limit}
        OFFSET {offset};
    """
    cursor.execute(sales_query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    movies = cleanTitle(columns, rows)

    cursor.close()
    conn.close()

    return movies

def fetch_bookable(limit = 50):
    conn = connect_db()
    cursor = conn.cursor()

    sales_query = f"""
        SELECT * FROM movies
        WHERE lower(status) = 'bookable'
        ORDER BY current_price ASC, title
        LIMIT {limit};
    """
    cursor.execute(sales_query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    movies = cleanTitle(columns, rows)

    cursor.close()
    conn.close()

    return movies

def cleanTitle(columns, rows):
    movies = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        row_dict['title'] = re.sub(r'\s*\(([^)]+)\)', '', row_dict['title'])
        movies.append(row_dict)

    return movies

@app.route('/')
def index():
    return render_template("index.html", sale_rows=sale_rows, sale_steelbooks = sale_steelbooks, bookable_movies = bookable)

@app.route('/getSale/<int:limit>/<int:offset>')
def getSale(limit, offset):
    return fetch_sale(limit, offset)

if __name__ == '__main__':
    sale_rows = fetch_sale(40, 0)
    sale_steelbooks = fetch_sale(40,0,"steelbook")
    bookable = fetch_bookable()
    app.run(debug=True, host="0.0.0.0", port="80")