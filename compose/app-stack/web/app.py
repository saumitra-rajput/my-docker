import os
from flask import Flask
import psycopg2
import redis

app = Flask(__name__)

# Environment Variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")

@app.route("/")
def home():
    try:
        # Connect to Postgres
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        conn.close()
        db_status = "Postgres Connected ✅"
    except Exception as e:
        db_status = f"Postgres Error ❌ {e}"

    try:
        # Connect to Redis
        r = redis.Redis(host=REDIS_HOST, port=6379)
        r.ping()
        redis_status = "Redis Connected ✅"
    except Exception as e:
        redis_status = f"Redis Error ❌ {e}"

    return f"""
    <h1>Hello from Flask 🚀</h1>
    <p>{db_status}</p>
    <p>{redis_status}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
