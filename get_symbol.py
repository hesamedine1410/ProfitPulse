import MetaTrader5 as mt5

if not mt5.initialize():
    print("Failed to get historical data:", mt5.last_error())
    exit()

symbols = mt5.symbols_get()
for symbol in symbols:
    print(symbol.name)

mt5.shutdown()
