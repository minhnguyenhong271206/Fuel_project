import sqlite3

# Kết nối database
connection = sqlite3.connect("fuel.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Calendar (
        date DATE PRIMARY KEY,
        day INTEGER,
        month INTEGER,
        quarter INTEGER,
        day_name VARCHAR,
        working_day BOOLEAN
    )
""")

cursor.execute(""" 
    CREATE TABLE IF NOT EXIST Product (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        category VARCHAR
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Market_Price (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        date DATE,
        price DECIMAL,
        unit VARCHAR,
        FOREIGN KEY (product_id) REFERENCES Product(id),
        FOREIGN KEY (date) REFERENCES Calendar(date)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS News (
        id INTEGER PRIMARY KEY,
        title VARCHAR,
        context TEXT,
        category VARCHAR,
        date DATE,
        FOREIGN KEY (date) REFERENCES Calendar(date)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS EconomicIndicator (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        value DECIMAL,
        unit VARCHAR,
        category VARCHAR,
        date DATE,
        FOREIGN KEY (date) REFERENCES Calendar(date)
    )
""")

connection.commit()
connection.close()


