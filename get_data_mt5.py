import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# شروع متاتریدر 5
# Start MetaTrader 5
if not mt5.initialize():
    print("Failed to connect to MetaTrader 5")
    print("Error:", mt5.last_error())
    exit()

# تعریف نماد و بازه زمانی
# Define symbol and timeframe
symbol = "EURUSD!"  # نماد معاملاتی  # Trading symbol
if not mt5.symbol_select(symbol):
    print(f"Received historical data for {symbol}:")
    mt5.shutdown()
    exit()

# تنظیم بازه زمانی
# Set time interval
timeframe = mt5.TIMEFRAME_M1 # 1 minute timeframe # تایم‌فریم 1 دقیقه
start_time = datetime(2024, 1, 1)  # شروع داده‌ها    # Start data
end_time = datetime(2024, 12, 31)  # پایان داده‌ها   # End data

# دریافت داده‌ها
# Get data
rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, start_time, end_time)
if rates is None:
    print("Failed to get historical data:", mt5.last_error())
else:
    for rate in rates:
        print(rate)

data = [
    (1704153600, 1.10401, 1.10427, 1.09378, 1.09392, 85877, 12, 0),
    # سایر داده‌ها...
]

for record in data:
    timestamp, open_price, high, low, close, tick_volume, spread, real_volume = record
    readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Time: {readable_time}, Open: {open_price}, High: {high}, Low: {low}, Close: {close}, Tick Volume: {tick_volume}, Spread: {spread}, Real Volume: {real_volume}")

# خاتمه اتصال
# Terminate connection
mt5.shutdown()