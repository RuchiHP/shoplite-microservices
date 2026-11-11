# This script creates a PostgreSQL table named "users" in the "usersdb" database.
# psycopg2 is a Python library that allows you to connect to PostgreSQL databases and execute SQL commands.
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="usersdb",
    user="shopuser",
    password="shoppass"
)

# cursor , is used to execute SQL commands and queries against the database
cur = conn.cursor()

# creating a table named "users" with columns for id, name, email, and created_at
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP      
)
""")

conn.commit()  # committing the changes to the database
cur.close()  # closing the cursor
conn.close()  # closing the database connection

print("Table 'users' created successfully.")