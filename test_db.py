from os import getenv
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOSTNAME"),
            port=getenv("DB_PORT"),
        )
        print("Connection to the database established successfully.")

        # Print all available tables
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        print("Available tables:")
        for table in tables:
            print(table[0])
        cursor.close()
        # Close the connection
        return connection
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        conn.close()