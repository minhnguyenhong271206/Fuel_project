from flask import Flask, Response, request
from flask_cors import CORS
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'fuel.db') 
#bien unit san pham và top 100
@app.route('/api/price')
def get_price():
    product_id = request.args.get('product_id')
    days = request.args.get('days')

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = "SELECT DISTINCT product_id, date, price, unit FROM MarketPrice"
    conditions = []
    params = []

    if product_id:
        conditions.append("product_id = ?")
        params.append(product_id)

    if days:
        conditions.append("""
            date >= (
                SELECT date(MAX(date), ?)
                FROM MarketPrice
            )
        """)
        params.append(f'-{days} days')

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY date ASC LIMIT 100"

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in data]

    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )


@app.route('/api/news')
def get_news():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM News LIMIT 100")
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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Calendar LIMIT 100")
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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM EconomicIndicator LIMIT 100")
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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product LIMIT 100")
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in data]
    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )

@app.route('/api/margin')
def get_margin():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Margin LIMIT 100")
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in data]
    connection.close()
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )

@app.route('/api/fullnews')
def get_fullnews():
    product_type = request.args.get('product_type')
    page = int(request.args.get('page', 1))
    limit = 20
    offset = (page - 1) * limit

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Đếm tổng số tin
    count_query = "SELECT COUNT(*) FROM FullNews"
    count_params = []
    if product_type:
        count_query += " WHERE product_type = ?"
        count_params.append(product_type)
    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]

    # Lấy data theo trang
    query = "SELECT * FROM FullNews"
    params = []
    if product_type:
        query += " WHERE product_type = ?"
        params.append(product_type)
    query += f" ORDER BY date_published DESC LIMIT {limit} OFFSET {offset}"

    cursor.execute(query, params)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in data]
    connection.close()

    return Response(
        json.dumps({'data': data, 'total': total, 'page': page, 'limit': limit}, ensure_ascii=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)