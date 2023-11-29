"""Imports sqlite3 functionality"""
import sqlite3


class DBOperations():
    """This class holds basic operations for a sqlite database"""

    def open_connection(self, connection_string):
        """Connects to the sqlite database."""
        try:
            conn = sqlite3.connect(connection_string)
            print("Opened database successfully.")
            return conn
        except Exception as e:
            print("Error opening db:", e)

    def create_cursor(self, db_connection):
        """Crates the cursor for the database."""
        try:
            cursor = db_connection.cursor()
            print("Cursor created successfully.")
            return cursor
        except Exception as e:
            print("Error created cursor:", e)

    def create_table(self, db_connection, cursor, table_format):
        """Creates the cursor to then create a new table in the database."""
        try:
            cursor.execute(table_format)
            db_connection.commit()
            print("Table created successfully.")
        except Exception as e:
            print("Error creating table:", e)

    def insert_into(self, db_connection, cursor, sql_string, data):
        """Inserts new data into the database."""
        try:
            sql = sql_string
            cursor.execute(sql, data)
            db_connection.commit()
            print("Added sample successfully.")
        except Exception as e:
            print("Error inserting sample.", e)

    def get_all_data(self, cursor):
        """Gets all the new data instered into the database."""
        try:
            for row in cursor.execute("select * from samples"):
                print(row)
            return cursor.execute("select * from samples")
        except Exception as e:
            print("Error fetching samples.", e)


if __name__ == "__main__":
    db = DBOperations()

    # Connect to the database.
    connection = db.open_connection("weather.sqlite")

    # Cartes the cursor for the database.
    cursor = db.create_cursor(connection)

    # Create new table with data provided.
    TABLE_FORMAT = """create table samples
                        (id integer primary key autoincrement not null,
                        date text not null,
                        location text not null,
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);"""
    db.create_table(connection, cursor, TABLE_FORMAT)

    # Insert new data into database.
    data_set_1 = ("2018-06-01", 'Winnipeg, MB', 12.0, 5.6, 7.1)
    data_set_2 = ("2018-06-02", 'Winnipeg, MB', 22.2, 11.1, 15.5)
    data_set_3 = ("2018-06-03", 'Winnipeg, MB', 31.3, 29.9, 30.0)
    SQL = """insert into samples (date,location,min_temp,max_temp,avg_temp)
                values (?,?,?,?,?)"""
    db.insert_into(connection, cursor, SQL, data_set_1)
    db.insert_into(connection, cursor, SQL, data_set_2)
    db.insert_into(connection, cursor, SQL, data_set_3)

    # Displays all data from database.
    db.get_all_data(cursor)
