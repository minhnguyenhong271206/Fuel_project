from flask import Flask, Response
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)
#bien unit san pham và top 100
@app.route('/api/price')
def get_price():
    connection = sqlite3.connect('fuel.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MarketPrice")
    data = cursor.fetchall()

    # Lấy tên cột
    columns = [column[0] for column in cursor.description]

    # Gộp tên cột với data
    data = [dict(zip(columns, row)) for row in data]

    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )


@app.route('/api/news')
def get_news():
    connection = sqlite3.connect('fuel.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM News")
    data = cursor.fetchall()

    # Lấy tên cột
    columns = [column[0] for column in cursor.description]

    # Gộp tên cột với data
    data = [dict(zip(columns, row)) for row in data]

    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )


@app.route('/api/calendar')
def get_calendar():
    connection = sqlite3.connect('fuel.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Calendar")
    data = cursor.fetchall()

    # Lấy tên cột
    columns = [column[0] for column in cursor.description]

    # Gộp tên cột với data
    data = [dict(zip(columns, row)) for row in data]

    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )


@app.route('/api/economic')
def get_economic():
    connection = sqlite3.connect('fuel.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM EconomicIndicator")
    data = cursor.fetchall()

    # Lấy tên cột
    columns = [column[0] for column in cursor.description]

    # Gộp tên cột với data
    data = [dict(zip(columns, row)) for row in data]

    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )

@app.route('/api/product')
def get_product():
    connection = sqlite3.connect('fuel.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product")
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in data]
    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)