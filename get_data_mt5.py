import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# اتصال به MT5
# Connect to MT5
if not mt5.initialize():
    print("Failed to initialize MT5, error code:", mt5.last_error())
    quit()

# بررسی اطلاعات درباره نماد
# Check information about the symbol
symbol = "ETHUSD"
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select {symbol}, error code:", mt5.last_error())
    quit()

# دریافت داده‌های قیمتی
# Get price data
timeframe = mt5.TIMEFRAME_H1  # تایم‌فریم یک‌ساعته    # One hour time frame
num_candles = 1000  # تعداد کندل‌ها      # Number of candles
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)

if rates is None:
    print(f"Failed to get rates for {symbol}, error code:", mt5.last_error())
    mt5.shutdown()
    quit()


# تبدیل داده‌ها به DataFrame
# Convert data to DataFrame
data = pd.DataFrame(rates)
data['time'] = pd.to_datetime(data['time'], unit='s')  # تبدیل زمان به فرمت خوانا   # Convert time to readable format

# نمایش داده‌ها
# Display data
print(data.head())

# ذخیره داده‌ها به فایل CSV
# Save data to CSV file
data.to_csv(f"{symbol}_data.csv", index=False)
print(f"Data saved to {symbol}_data.csv")

# خروج از MT5
# Exit MT5
mt5.shutdown()