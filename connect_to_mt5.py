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

import MetaTrader5 as mt5

# Initialize MT5
# MT5 را راه اندازی کنید
if not mt5.initialize():
    print(f"Failed to initialize MT5, error code: {mt5.last_error()}")
    quit()

# Login to MT5
# وارد MT5 شوید
login = 12345678  # شماره حساب  # Account number
password = "your_password"  # رمز عبور حساب     # Account password
server = "YourBroker-Server"  # سرور بروکر شما  # Your broker server

if not mt5.login(login, password, server):
    print(f"Failed to login, error: {mt5.last_error()}")
    mt5.shutdown()
    quit()

print("Successfully connected to MT5!")
mt5.shutdown()
