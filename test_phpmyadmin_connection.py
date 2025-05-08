import pymysql
import time

print("=== PyMySQL Test ===")

try:
    print("Connecting...")
    start = time.time()
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        port=3306,
        connect_timeout=5
    )
    end = time.time()
    print(f"✅ PyMySQL: Connection successful in {end - start:.2f} seconds.")
    conn.close()
except Exception as e:
    print("❌ PyMySQL Error:", e)
