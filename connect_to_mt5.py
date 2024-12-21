import MetaTrader5 as mt5

# شروع متاتریدر 5
# Start MetaTrader 5
if not mt5.initialize():
    print("Connection to MetaTrader 5 failed.")
    print("Error:", mt5.last_error())
    exit()

# اطلاعات حساب متصل‌شده
# Connected account information
account_info = mt5.account_info()
if account_info is not None:
    print("Your account information:")
    print("Login:", account_info.login)
    print("Balance:", account_info.balance)
    print("Leverage:", account_info.leverage)
else:
    print("Error retrieving account information")

# خاتمه اتصال
# Terminate connection
mt5.shutdown()