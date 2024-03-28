import sqlite3,os

def load_data_sqlite():
    
    #Remove old db file
    os.remove("sales.db")

    # Read data from file
    with open('data/total_sales_per_customer.csv', 'r') as file:
        lines = file.readlines()

    # Strip newline characters and split each line by comma
    data = [line.strip().split(',') for line in lines[1:]]

    # Convert data types as necessary
    formatted_data = [(int(row[0]), float(row[1])) for row in data]

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sales.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table to store the data
    cursor.execute('''CREATE TABLE IF NOT EXISTS total_sales_per_customer (
                        customer_id INTEGER PRIMARY KEY,
                        total_sales REAL
                    )''')

    # Insert data into the table
    cursor.executemany('INSERT INTO total_sales_per_customer VALUES (?, ?)', formatted_data)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    with open('data/AIQ - Data Engineer Assignment - Sales data.csv', 'r') as file:
        lines = file.readlines()

    # Strip newline characters and split each line by comma
    sales_data = [line.strip().split(',') for line in lines[1:]]

    # Convert data types as necessary
    #formatted_data = [(int(row[0]), float(row[1])) for row in data]

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sales.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table to store the data
    cursor.execute('''CREATE TABLE sales_data (
                        order_id INTEGER,
                        customer_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        price REAL,
                        order_date DATE
                    )
                    ''')

    # Insert data into the table
    cursor.executemany('INSERT INTO sales_data VALUES (?, ?, ?, ?, ?, ?)', sales_data)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    with open('data/AIQ - Data Engineer Assignment - Sales data.csv', 'r') as file:
        lines = file.readlines()

    # Strip newline characters and split each line by comma
    sales_data = [line.strip().split(',') for line in lines[1:]]

    # Convert data types as necessary
    #formatted_data = [(int(row[0]), float(row[1])) for row in data]

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sales.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table to store the data
    cursor.execute('''CREATE TABLE sales_data (
                        order_id INTEGER,
                        customer_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        price REAL,
                        order_date DATE
                    )
                    ''')

    # Insert data into the table
    cursor.executemany('INSERT INTO sales_data VALUES (?, ?, ?, ?, ?, ?)', sales_data)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


    print("Data has been stored in the SQLite database.")
