import sqlite3,os,json

def load_data_sqlite():
    
    #Remove old db file
    if os.path.exists('sales.db'):
        os.remove('sales.db')

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

    with open('data/user_data.csv', 'r') as file:
        lines = file.readlines()

    # Strip newline characters and split each line by comma
    user_data = [line.strip().split(',') for line in lines[1:]]

    # Convert data types as necessary
    #formatted_data = [(int(row[0]), float(row[1])) for row in data]

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sales.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
   
    # Create a table to store the data
    cursor.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    username TEXT,
                    email TEXT,
                    address TEXT,
                    phone TEXT,
                    website TEXT,
                    company TEXT
                )''')

    # Insert each row of data into the users table
    for row in user_data:
        # Convert nested JSON structures to strings
        address_str = json.dumps(row[4])
        company_str = json.dumps(row[7])
        
        # Insert data into the users table
        cursor.execute('''INSERT INTO users (id, name, username, email, address, phone, website, company) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (row[0], row[1], row[2], row[3], address_str, row[5], row[6], company_str))


    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

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

    # Read data from file
    with open('data/top_selling_products.csv', 'r') as file:
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_selling_product (
                        customer_id INTEGER PRIMARY KEY,
                        total_sales INTEGER
                    )''')

    # Insert data into the table
    cursor.executemany('INSERT INTO top_selling_product VALUES (?, ?)', formatted_data)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


    with open('data/merged.csv', 'r') as file:
        lines = file.readlines()

    # Strip newline characters and split each line by comma
    merged_data = [line.strip().split(',') for line in lines[1:]]

    # Convert data types as necessary
    #formatted_data = [(int(row[0]), float(row[1])) for row in data]

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sales.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
   
    # Create a table to store the data
    cursor.execute('''CREATE TABLE merged_user_data (
                    id INTEGER,
                    name TEXT,
                    username TEXT,
                    email TEXT,
                    address TEXT,
                    phone TEXT,
                    website TEXT,
                    company TEXT
                )''')

    # Insert each row of data into the users table
    for row in merged_data:
        # Convert nested JSON structures to strings
        address_str = json.dumps(row[4])
        company_str = json.dumps(row[7])
        
        # Insert data into the users table
        cursor.execute('''INSERT INTO merged_user_data (id, name, username, email, address, phone, website, company) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (row[0], row[1], row[2], row[3], address_str, row[5], row[6], company_str))


    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    print("Pipeline Complete. Data has been stored in the SQLite database.")
