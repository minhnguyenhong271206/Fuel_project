import pandas as pd
import sqlite3

excel_file = 'Gia_xang_dau-final_update_ngay.xlsx'
xl = pd.ExcelFile(excel_file)

connection = sqlite3.connect(DB_PATH)

# ==================== CALENDAR ====================
df_calendar = pd.read_excel(excel_file, sheet_name='12.DateTime')

df_calendar = df_calendar[['ListDate', 'Day', 'Month', 'Quarter', 'Day Name', 'Working Date Weekend']]
df_calendar = df_calendar.rename(columns={
    'ListDate'            : 'date',
    'Day'                 : 'day',
    'Month'               : 'month',
    'Quarter'             : 'quarter',
    'Day Name'            : 'day_name',
    'Working Date Weekend': 'working_day'
})

df_calendar['date'] = pd.to_datetime(df_calendar['date']).dt.date
df_calendar['working_day'] = df_calendar['working_day'].apply(lambda x: 1 if x == 'Working Day' else 0)

df_calendar = df_calendar.drop_duplicates(subset=['date'])

existing_dates = pd.read_sql("SELECT date FROM Calendar", connection)['date'].tolist()
df_calendar = df_calendar[~df_calendar['date'].astype(str).isin(existing_dates)]

if not df_calendar.empty:
    df_calendar.to_sql('Calendar', connection, if_exists='append', index=False)
    print(f"Đã import {len(df_calendar)} dòng vào bảng Calendar!")
else:
    print("Calendar: Không có dữ liệu mới để import.")

# ==================== PRODUCT ====================
df_product = pd.read_excel(excel_file, sheet_name='6.Gia SP_Daily')

df_product = df_product[['Product']].rename(columns={'Product': 'name'})
df_product = df_product.drop_duplicates(subset=['name'])

existing_products = pd.read_sql("SELECT name FROM Product", connection)['name'].tolist()
df_product = df_product[~df_product['name'].isin(existing_products)]

if not df_product.empty:
    df_product.to_sql('Product', connection, if_exists='append', index=False)
    print(f"Đã import {len(df_product)} dòng vào bảng Product!")
else:
    print("Product: Không có dữ liệu mới để import.")

# ==================== MARKET PRICE ====================
df_market_price = pd.read_excel(excel_file, sheet_name='6.Gia SP_Daily')

df_market_price = df_market_price[['Product', 'Time', 'Price', 'Unit']].rename(columns={
    'Product' : 'product_name',
    'Time'    : 'date',
    'Price'   : 'price',
    'Unit'    : 'unit'
})

df_market_price['date'] = pd.to_datetime(df_market_price['date']).dt.date

df_product_db = pd.read_sql("SELECT id, name FROM Product", connection)
df_market_price = df_market_price.merge(df_product_db, left_on='product_name', right_on='name', how='left')
df_market_price = df_market_price[['id', 'date', 'price', 'unit']].rename(columns={'id': 'product_id'})
df_market_price = df_market_price.dropna(subset=['product_id'])

# Lọc những cặp (product_id, date) chưa có trong DB
existing_mp = pd.read_sql("SELECT product_id, date FROM MarketPrice", connection)
existing_mp['product_id'] = existing_mp['product_id'].astype(str)
existing_mp['date'] = existing_mp['date'].astype(str)

df_market_price['product_id'] = df_market_price['product_id'].astype(str)
df_market_price['date_str'] = df_market_price['date'].astype(str)

existing_keys = set(zip(existing_mp['product_id'], existing_mp['date']))
mask = df_market_price.apply(
    lambda row: (row['product_id'], row['date_str']) not in existing_keys, axis=1
)
df_market_price = df_market_price[mask].drop(columns=['date_str'])

if not df_market_price.empty:
    df_market_price.to_sql('MarketPrice', connection, if_exists='append', index=False)
    print(f"Đã import {len(df_market_price)} dòng vào bảng MarketPrice!")
else:
    print("MarketPrice: Không có dữ liệu mới để import.")

# ==================== NEWS ====================
df_news = pd.read_excel(excel_file, sheet_name='8.Fertilizer News')

df_news = df_news[['Fertilizer', 'Market', 'Time']].rename(columns={
    'Fertilizer': 'title',
    'Market'    : 'category',
    'Time'      : 'date'
})

df_news['date'] = pd.to_datetime(df_news['date']).dt.date
df_news = df_news.dropna(subset=['title', 'date'])

existing_news = pd.read_sql("SELECT title, date FROM News", connection)
existing_news['date'] = existing_news['date'].astype(str)
df_news['date_str'] = df_news['date'].astype(str)

existing_news_keys = set(zip(existing_news['title'], existing_news['date']))
mask = df_news.apply(
    lambda row: (row['title'], row['date_str']) not in existing_news_keys, axis=1
)
df_news = df_news[mask].drop(columns=['date_str'])

if not df_news.empty:
    df_news.to_sql('News', connection, if_exists='append', index=False)
    print(f"Đã import {len(df_news)} dòng vào bảng News!")
else:
    print("News: Không có dữ liệu mới để import.")

# ==================== ECONOMIC INDICATOR ====================
df_economic = pd.read_excel(excel_file, sheet_name='7.DU_BAO gia dau tho-sp')

df_economic = df_economic[['Time', 'Name', 'Price']].rename(columns={
    'Time' : 'date',
    'Name' : 'name',
    'Price': 'value'
})

df_economic['date'] = pd.to_datetime(df_economic['date']).dt.date

existing_eco = pd.read_sql("SELECT name, date FROM EconomicIndicator", connection)
existing_eco['date'] = existing_eco['date'].astype(str)
df_economic['date_str'] = df_economic['date'].astype(str)

existing_eco_keys = set(zip(existing_eco['name'], existing_eco['date']))
mask = df_economic.apply(
    lambda row: (row['name'], row['date_str']) not in existing_eco_keys, axis=1
)
df_economic = df_economic[mask].drop(columns=['date_str'])

if not df_economic.empty:
    df_economic.to_sql('EconomicIndicator', connection, if_exists='append', index=False)
    print(f"Đã import {len(df_economic)} dòng vào bảng EconomicIndicator!")
else:
    print("EconomicIndicator: Không có dữ liệu mới để import.")


connection.commit()
connection.close()
print("Hoàn thành import toàn bộ dữ liệu!")
