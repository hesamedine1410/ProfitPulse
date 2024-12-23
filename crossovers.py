import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# شروع متاتریدر 5
if not mt5.initialize():
    print("Connection to MetaTrader 5 failed.")
    print("Error:", mt5.last_error())
    exit()

# دریافت داده‌ها (100 کندل 1 ساعته)
symbol = "EURUSD"  # نماد معاملاتی
timeframe = mt5.TIMEFRAME_H1  # تایم فریم 1 ساعته
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)  # گرفتن 100 کندل

# تبدیل داده‌ها به دیتا فریم pandas
rates_frame = pd.DataFrame(rates)
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
rates_frame.set_index('time', inplace=True)

# محاسبه میانگین متحرک کوتاه‌مدت (5) و بلندمدت (20)
rates_frame['SMA5'] = rates_frame['close'].rolling(window=5).mean()  # میانگین 5 کندل
rates_frame['SMA20'] = rates_frame['close'].rolling(window=20).mean()  # میانگین 20 کندل

# سیگنال خرید (کراس‌اوور صعودی) و فروش (کراس‌اوور نزولی)
rates_frame['Signal'] = np.where(rates_frame['SMA5'] > rates_frame['SMA20'], 1, 0)  # 1 برای خرید
rates_frame['Position'] = rates_frame['Signal'].diff()  # سیگنال خرید یا فروش (1 یا -1)

# نمایش سیگنال‌ها
print(rates_frame[['close', 'SMA5', 'SMA20', 'Position']].tail(10))  # آخرین سیگنال‌ها

# رسم نمودار
plt.figure(figsize=(10,6))
plt.plot(rates_frame.index, rates_frame['close'], label="Close Price")
plt.plot(rates_frame.index, rates_frame['SMA5'], label="SMA 5", color='orange')
plt.plot(rates_frame.index, rates_frame['SMA20'], label="SMA 20", color='green')

# نشان دادن سیگنال‌های خرید و فروش
plt.scatter(rates_frame.index[rates_frame['Position'] == 1], rates_frame['SMA5'][rates_frame['Position'] == 1], label="Buy Signal", marker='^', color='g')
plt.scatter(rates_frame.index[rates_frame['Position'] == -1], rates_frame['SMA5'][rates_frame['Position'] == -1], label="Sell Signal", marker='v', color='r')

plt.title(f'{symbol} - MA Crossover Strategy')
plt.legend(loc="best")
plt.show()

# خاتمه اتصال
mt5.shutdown()
