# wait_for_db.py
import sys
import time
from django.db import connections

def wait_for_db(max_retries=30):
    retry_count = 0
    while retry_count < max_retries:
        try:
            connections['default'].ensure_connection()
            print("Database is ready.")
            return
        except Exception as e:
            print(f"Database not ready, waiting... ({str(e)})")
            time.sleep(1)
            retry_count += 1

    print("Max retries reached. Exiting.")
    sys.exit(1)

if __name__ == "__main__":
    wait_for_db()
