import sqlite3
#Testing
class DBOperations:
    def __init__(self, db_file):
        self.db_file = db_file

    def initialize_db(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sample_date TEXT,
                    location TEXT,
                    min_temp REAL,
                    max_temp REAL,
                    avg_temp REAL,
                    UNIQUE(sample_date, location)
                )
            ''')
            conn.commit()
            conn.close()
            print("Database initialized successfully.")
        except Exception as e:
            print("Error initializing database:", e)

    def save_data(self, data):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO weather_data (sample_date, location, min_temp, max_temp, avg_temp)
                VALUES (?, ?, ?, ?, ?)
            ''', data)
            conn.commit()
            conn.close()
            print("Data saved successfully.")
        except Exception as e:
            print("Error saving data:", e)

    def purge_data(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM weather_data')
            conn.commit()
            conn.close()
            print("Data purged successfully.")
        except Exception as e:
            print("Error purging data:", e)

    def fetch_data(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM weather_data')
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            print("Error fetching data:", e)
            return None