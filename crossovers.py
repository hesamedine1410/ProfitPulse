import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# اتصال به MetaTrader 5
if not mt5.initialize():
    print("Connection to MetaTrader 5 failed.")
    print("Error:", mt5.last_error())
    exit()

# دریافت داده‌ها از کد get_data_mt5.py برای گروه‌های زمانی مختلف
symbol = "EURUSD!"  # نماد معاملاتی
timeframes = {
    "higher": {"primary": mt5.TIMEFRAME_M30, "alternate": mt5.TIMEFRAME_H1},
    "trading": {"primary": mt5.TIMEFRAME_M3, "alternate": mt5.TIMEFRAME_M5},
    "lower": {"primary": mt5.TIMEFRAME_M1},
}

# تابع برای دریافت داده‌های قیمت
def get_prices(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None:
        print(f"Failed to get rates for {symbol} on timeframe {timeframe}")
        return None
    return pd.DataFrame(rates)

# تعداد کندل‌ها برای هر تایم‌فریم (تعداد 100 کندل برای هر تایم‌فریم)
target_duration_hours = 100
candle_counts = {
    mt5.TIMEFRAME_M1: target_duration_hours * 60,
    mt5.TIMEFRAME_M3: target_duration_hours * 60 // 3,
    mt5.TIMEFRAME_M5: target_duration_hours * 60 // 5,
    mt5.TIMEFRAME_M30: target_duration_hours * 2,
    mt5.TIMEFRAME_H1: target_duration_hours,
}

# دریافت داده‌ها برای هر گروه زمانی
data = {}
for group, frames in timeframes.items():
    data[group] = {}
    for name, tf in frames.items():
        count = candle_counts[tf]
        prices = get_prices(symbol, tf, count)
        if prices is not None:
            if 'time' in prices.columns:
                prices['time'] = pd.to_datetime(prices['time'], unit='s')
                prices.set_index('time', inplace=True)
            else:
                print(f"Time column not found for {group} - {name}")
                continue
            data[group][name] = prices
            print(f"Data for {group} - {name}:")
            print(prices.head())
        else:
            print(f"No data for {group} - {name}.")

# انتخاب داده‌ها برای تایم فریم 1 ساعته از داده‌های "higher"
rates_frame = data['higher']['primary']

# محاسبه میانگین متحرک کوتاه‌مدت (5) و بلندمدت (21)
rates_frame['SMA5'] = rates_frame['close'].rolling(window=5).mean()  # میانگین 5 کندل
rates_frame['SMA21'] = rates_frame['close'].rolling(window=21).mean()  # میانگین 21 کندل

# محاسبه RSI (13 روزه)
def compute_rsi(data, window=13):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

rates_frame['RSI'] = compute_rsi(rates_frame['close'], window=13)

# محاسبه MACD (12 و 26)
rates_frame['EMA12'] = rates_frame['close'].ewm(span=12, adjust=False).mean()
rates_frame['EMA26'] = rates_frame['close'].ewm(span=26, adjust=False).mean()
rates_frame['MACD'] = rates_frame['EMA12'] - rates_frame['EMA26']
rates_frame['Signal_Line'] = rates_frame['MACD'].ewm(span=9, adjust=False).mean()

# سیگنال خرید (کراس‌اوور صعودی) و فروش (کراس‌اوور نزولی) با ترکیب SMA و RSI
rates_frame['Signal'] = np.where((rates_frame['SMA5'] > rates_frame['SMA21']) & (rates_frame['RSI'] < 30), 1, 0)  # 1 برای خرید
rates_frame['Position'] = rates_frame['Signal'].diff()  # سیگنال خرید یا فروش (1 یا -1)

# نمایش سیگنال‌ها
print(rates_frame[['close', 'SMA5', 'SMA21', 'RSI', 'MACD', 'Signal_Line', 'Position']].tail(10))  # آخرین سیگنال‌ها

# رسم نمودار
plt.figure(figsize=(10, 6))

# نمودار قیمت و میانگین‌های متحرک
plt.subplot(2, 1, 1)
plt.plot(rates_frame.index, rates_frame['close'], label="Close Price")
plt.plot(rates_frame.index, rates_frame['SMA5'], label="SMA 5", color='orange')
plt.plot(rates_frame.index, rates_frame['SMA21'], label="SMA 21", color='green')

# نشان دادن سیگنال‌های خرید و فروش
plt.scatter(rates_frame.index[rates_frame['Position'] == 1], rates_frame['SMA5'][rates_frame['Position'] == 1], label="Buy Signal", marker='^', color='g')
plt.scatter(rates_frame.index[rates_frame['Position'] == -1], rates_frame['SMA5'][rates_frame['Position'] == -1], label="Sell Signal", marker='v', color='r')

plt.title(f'{symbol} - MA Crossover with RSI Strategy')
plt.legend(loc="best")

# نمودار MACD
plt.subplot(2, 1, 2)
plt.plot(rates_frame.index, rates_frame['MACD'], label="MACD", color='blue')
plt.plot(rates_frame.index, rates_frame['Signal_Line'], label="Signal Line", color='red')
plt.bar(rates_frame.index, rates_frame['MACD'] - rates_frame['Signal_Line'], label="MACD Histogram", color='gray', alpha=0.3)

plt.title(f'{symbol} - MACD and Signal Line')
plt.legend(loc="best")

plt.tight_layout()
plt.show()

# خاتمه اتصال
mt5.shutdown()
