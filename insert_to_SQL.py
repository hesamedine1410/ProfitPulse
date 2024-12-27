import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
import mysql.connector
from dotenv import load_dotenv

# بارگذاری متغیرها از فایل .env
load_dotenv()
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# اتصال به پایگاه داده MySQL
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

# ایجاد جداول در پایگاه داده
cursor.execute("""
CREATE TABLE IF NOT EXISTS timeframe_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    timeframe VARCHAR(10),
    time DATETIME,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    tick_volume INT,
    spread INT,
    real_volume INT
);
""")
conn.commit()

# اتصال به MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5.")
    quit()

# تابع برای دریافت داده‌های قیمت
def get_prices(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None:
        print(f"Failed to get rates for {symbol} on timeframe {timeframe}")
        return None
    prices = pd.DataFrame(rates)
    prices['time'] = pd.to_datetime(prices['time'], unit='s')  # تبدیل زمان به فرمت قابل‌خواندن
    return prices

# تنظیم تایم‌فریم‌ها و تعداد کندل‌ها
timeframes = {
    "higher": mt5.TIMEFRAME_M30,  # بلندمدت (30 دقیقه)
    "review": mt5.TIMEFRAME_M5,   # بررسی (5 دقیقه)
    "lower": mt5.TIMEFRAME_M1,    # کوتاه‌مدت (1 دقیقه)
}
candle_counts = {
    "higher": 336,    # 30 دقیقه‌ای: 336 کندل (7 روز)
    "review": 2016,   # 5 دقیقه‌ای: 2016 کندل (7 روز)
    "lower": 10080,   # 1 دقیقه‌ای: 10080 کندل (7 روز)
}

# سیمبل موردنظر
symbol = "ETHUSD"

# دریافت داده‌ها و وارد کردن به پایگاه داده
for key, tf in timeframes.items():
    count = candle_counts[key]
    prices = get_prices(symbol, tf, count)
    if prices is not None:
        print(f"Inserting data for {key} timeframe into database...")
        for _, row in prices.iterrows():
            # تبدیل زمان به فرمت مناسب برای MySQL
            row['time'] = row['time'].strftime('%Y-%m-%d %H:%M:%S')
            
            try:
                cursor.execute("""
                INSERT INTO timeframe_data (symbol, timeframe, time, open, high, low, close, tick_volume, spread, real_volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    symbol, key, row['time'], row['open'], row['high'], row['low'], row['close'], 
                    row['tick_volume'], row['spread'], row['real_volume']
                ))
                conn.commit()
            except Exception as e:
                print(f"Error inserting data: {e}")
        print(f"Data for {key} timeframe inserted successfully.")
    else:
        print(f"Failed to retrieve data for {key} timeframe.")
# بستن اتصال‌ها
cursor.close()
conn.close()
mt5.shutdown()