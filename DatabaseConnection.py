import psycopg2

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "database": "gainztracker",
    "user": "your_username",
    "password": "your_password",
}


def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None


def save_entry(date, category, detail, value):
    """Save a new entry to the database."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO logs (date, category, detail, value) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (date, category, detail, value))
            conn.commit()
            cursor.close()
            print("Entry saved successfully.")
        except Exception as e:
            print("Error saving entry:", e)
        finally:
            conn.close()


def fetch_all_logs():
    """Fetch all logs from the database."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY date DESC")
            logs = cursor.fetchall()
            cursor.close()
            return logs
        except Exception as e:
            print("Error fetching logs:", e)
        finally:
            conn.close()
    return []
