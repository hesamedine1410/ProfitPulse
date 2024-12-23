from dotenv import load_dotenv
import os
import mysql.connector

# بارگذاری متغیرها از فایل .env
load_dotenv()

# دریافت مقادیر از متغیرهای محیطی
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

# ایجاد یک شی cursor برای تعامل با پایگاه داده
cursor = conn.cursor()

# ایجاد پایگاه داده
cursor.execute("CREATE DATABASE IF NOT EXISTS my_database;")

# استفاده از پایگاه داده
cursor.execute("USE my_database;")

# ایجاد جدول
cursor.execute("""
CREATE TABLE IF NOT EXISTS my_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT
);
""")

# ذخیره تغییرات
conn.commit()

# بستن اتصال
cursor.close()
conn.close()
