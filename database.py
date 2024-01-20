import os
import sqlite3
from tabulate import tabulate

DB_NAME = 'book_db.db'

def create_db(datafolder='./data/'):
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    order_of_files = ["sql_create_queries.txt", "sql_insert_queries.txt"]
    for file in order_of_files:
        filepath = os.path.join(datafolder, file)
        execute_queries_from_file(filepath)
    print(f"{DB_NAME} is created")

# Function to execute SQL queries from a file
def execute_queries_from_file(filename):
    # Create or connect to the SQLite database
    connection = sqlite3.connect(DB_NAME)
    with open(filename, 'r') as file:
        queries = file.read().split(';')  # Split queries by semicolon
        for query in queries:
            if query.strip():  # Skip empty queries
                connection.execute(query)
    # Commit changes and close the connection
    connection.commit()
    connection.close()


def execute_sql_queries(queries):
    try:
        # Create or connect to the SQLite database
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        for query in queries.split(';'):  # Split queries by semicolon
            query = query.strip()
            if query:
                print(f"Going to execute:")
                print(query)
                if query.lower().startswith('select'):
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if rows:
                        headers = [description[0] for description in cursor.description]
                        print(tabulate(rows, headers, tablefmt='grid'))  # Print as a table
                else:
                    cursor.execute(query)
        connection.commit()
    except sqlite3.Error as e:
        if connection:
            connection.rollback()
        print(f"Error executing queries: {e} with {query}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_db()
    datafolder = './data/'
    order_of_files = ["sql_update_queries.txt", "sql_select_queries.txt"]
    for file in order_of_files:
        filepath = os.path.join(datafolder, file)
        with open(filepath, 'r') as f:
            queries = f.read()  # Split queries by semicolon
            execute_sql_queries(queries)
