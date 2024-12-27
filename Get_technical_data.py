import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import talib as ta
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# بارگذاری متغیرها از فایل .env
load_dotenv()
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# داده‌های فرضی کندل
data = {
    "timestamp": pd.date_range(start="2024-12-19", periods=336, freq="30min"),
    "open": np.random.rand(336) * 100,
    "high": np.random.rand(336) * 100,
    "low": np.random.rand(336) * 100,
    "close": np.random.rand(336) * 100,
    "volume": np.random.randint(1, 1000, size=336)
}
df_30min = pd.DataFrame(data)

# تابع محاسبه شاخص‌های تکنیکال
def calculate_indicators(df):
    df['MA_50'] = ta.SMA(df['close'], timeperiod=50)
    df['MA_200'] = ta.SMA(df['close'], timeperiod=200)
    df['EMA_9'] = ta.EMA(df['close'], timeperiod=9)
    df['RSI_14'] = ta.RSI(df['close'], timeperiod=14)
    df['RSI_7'] = ta.RSI(df['close'], timeperiod=7)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = ta.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df = df.bfill()
    return df

# تابع ذخیره داده‌ها
def save_to_mysql(df):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            sql = """INSERT INTO indicators_data (timestamp, close, MA_50, MA_200, EMA_9, RSI_14, RSI_7, MACD, MACD_signal, MACD_hist, BB_upper, BB_middle, BB_lower)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (row['timestamp'], row['close'], row['MA_50'], row['MA_200'], row['EMA_9'],
                      row['RSI_14'], row['RSI_7'], row['MACD'], row['MACD_signal'], row['MACD_hist'],
                      row['BB_upper'], row['BB_middle'], row['BB_lower'])
            cursor.execute(sql, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

# اجرا
df_30min = calculate_indicators(df_30min)
save_to_mysql(df_30min)
print("Data saved successfully.")
