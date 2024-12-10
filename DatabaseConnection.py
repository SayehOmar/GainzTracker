import psycopg2


class DatabaseManager:
    def __init__(self):
        # Update with your PostgreSQL credentials
        self.connection = psycopg2.connect(
            dbname="GainzTracker",  # Database name
            user="postgres",  # Replace with your username
            password="0000",  # Replace with your password
            host="localhost",
            port="5432",  # Default PostgreSQL port
        )
        self.cursor = self.connection.cursor()

    def insert_data(self, date, workout, creatine_intake, weight):
        try:
            query = """
            INSERT INTO user_data (date, workout, creatine_intake, weight)
            VALUES (%s, %s, %s, %s);
            """
            self.cursor.execute(query, (date, workout, creatine_intake, weight))
            self.connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("Error inserting data:", e)

    def close(self):
        self.cursor.close()
        self.connection.close()
