import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

# تعریف تایم‌فریم‌ها
timeframes = {
    "higher": {"primary": mt5.TIMEFRAME_M30, "alternate": mt5.TIMEFRAME_H1},
    "trading": {"primary": mt5.TIMEFRAME_M3, "alternate": mt5.TIMEFRAME_M5},
    "lower": {"primary": mt5.TIMEFRAME_M1},
}

# اتصال به MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5.")
    quit()

# تابع برای دریافت داده‌های قیمت
def get_prices(symbol, timeframe, count):
    """دریافت داده‌های قیمت برای یک سیمبل و تایم‌فریم مشخص."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None:
        print(f"Failed to get rates for {symbol} on timeframe {timeframe}")
        return None
    return pd.DataFrame(rates)

# تعیین تعداد کندل‌ها به گونه‌ای که مدت زمان کل برابر باشد
target_duration_hours = 100  # مدت زمان معادل برای همه تایم‌فریم‌ها (به ساعت)

# تعداد کندل‌ها برای هر تایم‌فریم را تنظیم می‌کنیم
candle_counts = {
    mt5.TIMEFRAME_M1: target_duration_hours * 60,  # 1 دقیقه‌ای
    mt5.TIMEFRAME_M3: target_duration_hours * 60 // 3,  # 3 دقیقه‌ای
    mt5.TIMEFRAME_M5: target_duration_hours * 60 // 5,  # 5 دقیقه‌ای
    mt5.TIMEFRAME_M30: target_duration_hours * 2,  # 30 دقیقه‌ای
    mt5.TIMEFRAME_H1: target_duration_hours,  # 1 ساعته
}

# دریافت داده‌ها برای هر گروه زمانی
symbol = "EURUSD!"  # سیمبل موردنظر
data = {}

for group, frames in timeframes.items():
    data[group] = {}
    for name, tf in frames.items():
        count = candle_counts[tf]
        prices = get_prices(symbol, tf, count)
        if prices is not None:
            # بررسی اینکه ستون time در دیتافریم وجود دارد
            if 'time' in prices.columns:
                # تبدیل زمان به فرمت قابل‌خواندن
                prices['time'] = pd.to_datetime(prices['time'], unit='s')
            else:
                print(f"Time column not found for {group} - {name}")
                continue
            data[group][name] = prices
            print(f"Data for {group} - {name}:")
            print(prices.head())
        else:
            print(f"No data for {group} - {name}.")

# قطع اتصال
mt5.shutdown()

# ذخیره داده‌ها به فایل CSV (اختیاری)
for group, frames in data.items():
    for name, df in frames.items():
        df.to_csv(f"{symbol}_{group}_{name}.csv", index=False)
