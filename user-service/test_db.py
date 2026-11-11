
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="usersdb",
    user="shopuser",
    password="shoppass"
)

print("Database connection established successfully.")
conn.close()