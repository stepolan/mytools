# ./tools/fakedata/fake_data_multiple_dbs.py

import mysql.connector
from faker import Faker
import random
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Faker
fake = Faker()

# Define database names and table distribution
databases = {
    'crmdb': [
        'customers',
        'leads',
        'interactions',
        'orders'
    ],
    'erpdb': [
        'suppliers',
        'products',
        'shippers',
        'inventory',
        'product_shipper'
    ],
    'hrdb': [
        'departments',
        'employees'
    ],
    'financedb': [
        'invoices',
        'payments'
    ],
    'marketingdb': [
        'campaigns',
        'ad_spends',
        'customer_engagements'
    ],
    'salesdb': [
        'sales_teams',
        'sales_targets',
        'sales_performance'
    ],
    'itdb': [
        'assets',
        'tickets',
        'projects',
        'users'
    ]
}

# Placeholder to store primary keys for generated data
data_store = {
    'customers': [],
    'leads': [],
    'departments': [],
    'orders': [],
    'invoices': [],
    'campaigns': [],
    'employees': [],
    'assets': [],
    'suppliers': [],
    'products': [],
    'sales_teams': [],
    'shippers': []
}

# Define table schemas and data generation logic
table_schemas_and_data = {
    'customers': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100),
                phone VARCHAR(20),
                company VARCHAR(100),
                address TEXT,
                city VARCHAR(50),
                state VARCHAR(50),
                postal_code VARCHAR(20),
                country VARCHAR(50)
            )
        """,
        'data': lambda: (
            truncate_value(fake.first_name(), 50),
            truncate_value(fake.last_name(), 50),
            truncate_value(fake.email(), 100),
            truncate_value(fake.phone_number(), 20),
            truncate_value(fake.company(), 100),
            truncate_value(fake.address(), 255),
            truncate_value(fake.city(), 50),
            truncate_value(fake.state(), 50),
            truncate_value(fake.postcode(), 20),
            truncate_value(fake.country(), 50)
        ),
        'store_key': lambda cursor: data_store['customers'].append(cursor.lastrowid)
    },
    'leads': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Leads (
                lead_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100),
                phone VARCHAR(20),
                company VARCHAR(100),
                interest_level VARCHAR(20)
            )
        """,
        'data': lambda: (
            truncate_value(fake.first_name(), 50),
            truncate_value(fake.last_name(), 50),
            truncate_value(fake.email(), 100),
            truncate_value(fake.phone_number(), 20),
            truncate_value(fake.company(), 100),
            truncate_value(fake.random_element(['High', 'Medium', 'Low']), 20)
        ),
        'store_key': lambda cursor: data_store['leads'].append(cursor.lastrowid)
    },
    'interactions': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Interactions (
                interaction_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                lead_id INT,
                date TIMESTAMP,
                interaction_type VARCHAR(50),
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (lead_id) REFERENCES Leads(lead_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['customers']),
            random.choice(data_store['leads']),
            fake.date_time_this_decade(),
            truncate_value(fake.random_element(['Email', 'Phone Call', 'Meeting', 'Demo']), 50),
            truncate_value(fake.text(), 255)
        )
    },
    'orders': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                order_date TIMESTAMP,
                required_date TIMESTAMP,
                shipped_date TIMESTAMP,
                ship_via INT,
                freight DECIMAL(10, 2),
                ship_name VARCHAR(100),
                ship_address TEXT,
                ship_city VARCHAR(50),
                ship_region VARCHAR(50),
                ship_postal_code VARCHAR(20),
                ship_country VARCHAR(50),
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['customers']),
            fake.date_time_this_decade(),
            fake.date_time_this_decade(),
            fake.date_time_this_decade(),
            random.randint(1, 3),
            round(random.uniform(10.0, 1000.0), 2),
            truncate_value(fake.company(), 100),
            truncate_value(fake.address(), 255),
            truncate_value(fake.city(), 50),
            truncate_value(fake.state(), 50),
            truncate_value(fake.postcode(), 20),
            truncate_value(fake.country(), 50)
        ),
        'store_key': lambda cursor: data_store['orders'].append(cursor.lastrowid)
    },
    'suppliers': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Suppliers (
                supplier_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(100),
                contact_name VARCHAR(50),
                contact_title VARCHAR(50),
                address TEXT,
                city VARCHAR(50),
                region VARCHAR(50),
                postal_code VARCHAR(20),
                country VARCHAR(50),
                phone VARCHAR(25),
                fax VARCHAR(25),
                homepage TEXT
            )
        """,
        'data': lambda: (
            truncate_value(fake.company(), 100),
            truncate_value(fake.name(), 50),
            truncate_value(fake.job(), 50),
            truncate_value(fake.address(), 255),
            truncate_value(fake.city(), 50),
            truncate_value(fake.state(), 50),
            truncate_value(fake.postcode(), 20),
            truncate_value(fake.country(), 50),
            truncate_value(fake.phone_number(), 25),
            truncate_value(fake.phone_number(), 25),
            truncate_value(fake.url(), 255)
        ),
        'store_key': lambda cursor: data_store['suppliers'].append(cursor.lastrowid)
    },
    'products': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(100),
                supplier_id INT,
                category_id INT,
                quantity_per_unit VARCHAR(50),
                unit_price DECIMAL(10, 2),
                units_in_stock INT,
                units_on_order INT,
                reorder_level INT,
                discontinued BOOLEAN,
                FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
            )
        """,
        'data': lambda: (
            truncate_value(fake.word(), 100),
            random.choice(data_store['suppliers']),
            random.randint(1, 10),
            str(random.randint(1, 100)),  # Ensure quantity_per_unit is a string
            round(random.uniform(1.0, 100.0), 2),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 100),
            fake.boolean()
        ),
        'store_key': lambda cursor: data_store['products'].append(cursor.lastrowid)
    },
    'shippers': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Shippers (
                shipper_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(50),
                phone VARCHAR(25)
            )
        """,
        'data': lambda: (
            truncate_value(fake.company(), 50),
            truncate_value(fake.phone_number(), 25)
        ),
        'store_key': lambda cursor: data_store['shippers'].append(cursor.lastrowid)
    },
    'inventory': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Inventory (
                inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                region VARCHAR(50),
                stock_level INT,
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['products']),
            truncate_value(fake.state(), 50),
            random.randint(0, 1000)
        )
    },
    'product_shipper': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Product_Shipper (
                product_shipper_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                shipper_id INT,
                FOREIGN KEY (product_id) REFERENCES Products(product_id),
                FOREIGN KEY (shipper_id) REFERENCES Shippers(shipper_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['products']),
            random.choice(data_store['shippers'])
        )
    },
    'departments': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Departments (
                department_id INT AUTO_INCREMENT PRIMARY KEY,
                department_name VARCHAR(50),
                manager_id INT,
                location_id INT
            )
        """,
        'data': lambda: (
            truncate_value(fake.word(), 50),
            random.randint(1, 100),
            random.randint(1, 100)
        ),
        'store_key': lambda cursor: data_store['departments'].append(cursor.lastrowid)
    },
    'employees': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Employees (
                employee_id INT AUTO_INCREMENT PRIMARY KEY,
                last_name VARCHAR(50),
                first_name VARCHAR(50),
                title VARCHAR(50),
                title_of_courtesy VARCHAR(25),
                birth_date DATE,
                hire_date DATE,
                address TEXT,
                city VARCHAR(50),
                region VARCHAR(50),
                postal_code VARCHAR(20),
                country VARCHAR(50),
                home_phone VARCHAR(25),
                extension VARCHAR(10),
                notes TEXT,
                department_id INT,
                FOREIGN KEY (department_id) REFERENCES Departments(department_id)
            )
        """,
        'data': lambda: (
            truncate_value(fake.last_name(), 50),
            truncate_value(fake.first_name(), 50),
            truncate_value(fake.job(), 50),
            truncate_value(fake.prefix(), 25),
            fake.date_of_birth().strftime('%Y-%m-%d'),
            fake.date_this_century().strftime('%Y-%m-%d'),
            truncate_value(fake.address(), 255),
            truncate_value(fake.city(), 50),
            truncate_value(fake.state(), 50),
            truncate_value(fake.postcode(), 20),
            truncate_value(fake.country(), 50),
            truncate_value(fake.phone_number(), 25),
            str(fake.random_int(min=100, max=9999)),
            truncate_value(fake.text(), 255),
            random.choice(data_store['departments'])
        ),
        'store_key': lambda cursor: data_store['employees'].append(cursor.lastrowid)
    },
    'invoices': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Invoices (
                invoice_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                invoice_date TIMESTAMP,
                due_date TIMESTAMP,
                total DECIMAL(10, 2),
                FOREIGN KEY (order_id) REFERENCES Orders(order_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['orders']),
            fake.date_time_this_decade(),
            fake.date_time_this_decade(),
            round(random.uniform(100.0, 10000.0), 2)
        ),
        'store_key': lambda cursor: data_store['invoices'].append(cursor.lastrowid)
    },
    'payments': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                invoice_id INT,
                payment_date TIMESTAMP,
                amount DECIMAL(10, 2),
                payment_method VARCHAR(50),
                FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['invoices']),
            fake.date_time_this_decade(),
            round(random.uniform(100.0, 10000.0), 2),
            truncate_value(fake.random_element(['Credit Card', 'Wire Transfer', 'PayPal']), 50)
        )
    },
    'campaigns': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Campaigns (
                campaign_id INT AUTO_INCREMENT PRIMARY KEY,
                campaign_name VARCHAR(100),
                start_date DATE,
                end_date DATE,
                budget DECIMAL(10, 2)
            )
        """,
        'data': lambda: (
            truncate_value(fake.catch_phrase(), 100),
            fake.date_this_year().strftime('%Y-%m-%d'),
            fake.date_this_year().strftime('%Y-%m-%d'),
            round(random.uniform(1000.0, 100000.0), 2)
        ),
        'store_key': lambda cursor: data_store['campaigns'].append(cursor.lastrowid)
    },
    'ad_spends': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Ad_Spends (
                ad_spend_id INT AUTO_INCREMENT PRIMARY KEY,
                campaign_id INT,
                amount_spent DECIMAL(10, 2),
                date_spent DATE,
                FOREIGN KEY (campaign_id) REFERENCES Campaigns(campaign_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['campaigns']),
            round(random.uniform(100.0, 10000.0), 2),
            fake.date_this_year().strftime('%Y-%m-%d')
        )
    },
    'customer_engagements': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Customer_Engagements (
                engagement_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                campaign_id INT,
                engagement_date DATE,
                engagement_type VARCHAR(50),
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (campaign_id) REFERENCES Campaigns(campaign_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['customers']),
            random.choice(data_store['campaigns']),
            fake.date_this_year().strftime('%Y-%m-%d'),
            truncate_value(fake.random_element(['Email', 'Phone Call', 'Social Media', 'Webinar']), 50)
        )
    },
    'sales_teams': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Sales_Teams (
                team_id INT AUTO_INCREMENT PRIMARY KEY,
                team_name VARCHAR(100),
                manager_id INT,
                FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
            )
        """,
        'data': lambda: (
            truncate_value(fake.catch_phrase(), 100),
            random.choice(data_store['employees'])
        ),
        'store_key': lambda cursor: data_store['sales_teams'].append(cursor.lastrowid)
    },
    'sales_targets': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Sales_Targets (
                target_id INT AUTO_INCREMENT PRIMARY KEY,
                team_id INT,
                target_amount DECIMAL(10, 2),
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (team_id) REFERENCES Sales_Teams(team_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['sales_teams']),
            round(random.uniform(10000.0, 1000000.0), 2),
            fake.date_this_year().strftime('%Y-%m-%d'),
            fake.date_this_year().strftime('%Y-%m-%d')
        )
    },
    'sales_performance': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Sales_Performance (
                performance_id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT,
                target_id INT,
                sales_amount DECIMAL(10, 2),
                date DATE,
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
                FOREIGN KEY (target_id) REFERENCES Sales_Targets(target_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['employees']),
            random.choice(data_store['sales_targets']),
            round(random.uniform(1000.0, 100000.0), 2),
            fake.date_this_year().strftime('%Y-%m-%d')
        )
    },
    'assets': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Assets (
                asset_id INT AUTO_INCREMENT PRIMARY KEY,
                asset_name VARCHAR(100),
                asset_type VARCHAR(50),
                purchase_date DATE,
                value DECIMAL(10, 2),
                employee_id INT,
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
            )
        """,
        'data': lambda: (
            truncate_value(fake.catch_phrase(), 100),
            truncate_value(fake.word(), 50),
            fake.date_this_decade().strftime('%Y-%m-%d'),
            round(random.uniform(100.0, 10000.0), 2),
            random.choice(data_store['employees'])
        ),
        'store_key': lambda cursor: data_store['assets'].append(cursor.lastrowid)
    },
    'tickets': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Tickets (
                ticket_id INT AUTO_INCREMENT PRIMARY KEY,
                asset_id INT,
                issue VARCHAR(255),
                reported_date DATE,
                resolution_date DATE,
                status VARCHAR(50),
                FOREIGN KEY (asset_id) REFERENCES Assets(asset_id)
            )
        """,
        'data': lambda: (
            random.choice(data_store['assets']),
            truncate_value(fake.sentence(), 255),
            fake.date_this_year().strftime('%Y-%m-%d'),
            fake.date_this_year().strftime('%Y-%m-%d'),
            truncate_value(fake.random_element(['Open', 'Closed', 'Pending']), 50)
        )
    },
    'projects': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Projects (
                project_id INT AUTO_INCREMENT PRIMARY KEY,
                project_name VARCHAR(100),
                start_date DATE,
                end_date DATE,
                budget DECIMAL(10, 2),
                manager_id INT,
                FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
            )
        """,
        'data': lambda: (
            truncate_value(fake.catch_phrase(), 100),
            fake.date_this_year().strftime('%Y-%m-%d'),
            fake.date_this_year().strftime('%Y-%m-%d'),
            round(random.uniform(10000.0, 1000000.0), 2),
            random.choice(data_store['employees'])
        )
    },
    'users': {
        'schema': """
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(255),
                employee_id INT,
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
            )
        """,
        'data': lambda: (
            truncate_value(fake.user_name(), 50),
            truncate_value(fake.password(), 255),
            random.choice(data_store['employees'])
        )
    }
}

db_config_template = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'auth_plugin': 'caching_sha2_password'
}

def create_databases():
    db_config = db_config_template.copy()
    db_config.pop('database', None)  # Remove the database key to connect to the server

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for db_name in databases.keys():
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            logging.info(f"Database {db_name} checked/created.")
        conn.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def truncate_value(value, max_length):
    if isinstance(value, str):
        return value[:max_length]
    return str(value)[:max_length]

def create_tables_sequentially():
    ordered_table_list = [
        'customers', 'leads', 'interactions', 'orders',  # crmdb
        'suppliers', 'products', 'shippers', 'inventory', 'product_shipper',  # erpdb
        'departments', 'employees',  # hrdb
        'invoices', 'payments',  # financedb
        'campaigns', 'ad_spends', 'customer_engagements',  # marketingdb
        'sales_teams', 'sales_targets', 'sales_performance',  # salesdb
        'assets', 'tickets', 'projects', 'users'  # itdb
    ]

    for db_name, tables in databases.items():
        db_config = db_config_template.copy()
        db_config['database'] = db_name

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks
            for table_name in ordered_table_list:
                if table_name in tables:
                    cursor.execute(table_schemas_and_data[table_name]['schema'])
                    logging.info(f"Table {table_name} created in database {db_name}.")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Enable foreign key checks
            conn.commit()
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def create_and_populate_table(db_name, table_name, num_rows):
    db_config = db_config_template.copy()
    db_config['database'] = db_name

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks
        cursor.execute(f"USE {db_name}")
        cursor.execute(table_schemas_and_data[table_name]['schema'])

        insert_query = """
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        """.format(
            table_name=table_name.split('_')[0].capitalize(),
            columns=', '.join([key for key in table_schemas_and_data[table_name]['data']()]),
            placeholders=', '.join(['%s'] * len(table_schemas_and_data[table_name]['data']()))
        )

        for _ in range(num_rows):
            cursor.execute(insert_query, table_schemas_and_data[table_name]['data']())
            if 'store_key' in table_schemas_and_data[table_name]:
                table_schemas_and_data[table_name]['store_key'](cursor)

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Enable foreign key checks
        conn.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    logging.info(f"Table {table_name} created and populated with {num_rows} rows.")

def main():
    create_databases()  # Ensure databases are created
    create_tables_sequentially()  # Create tables sequentially

    num_customers = int(input("Enter the number of customers: ").strip() or 500)
    
    # Calculate the number of rows for each table based on the ratios
    num_rows_dict = {
        'customers': num_customers,
        'leads': int(num_customers * 1.5),
        'interactions': int(num_customers * 3),
        'products': int(num_customers * 10),
        'orders': int(num_customers * 5),
        'suppliers': int(num_customers * 10 * 0.1),
        'shippers': int(num_customers * 10 * 0.05),
        'employees': int(num_customers * 0.2),
        'departments': int(num_customers * 0.2 * 0.05),
        'invoices': int(num_customers * 5),
        'payments': int(num_customers * 5),
        'campaigns': int(num_customers * 0.1),
        'ad_spends': int(num_customers * 0.2),
        'customer_engagements': int(num_customers * 0.3),
        'sales_teams': int(num_customers * 0.05),
        'sales_targets': int(num_customers * 0.1),
        'sales_performance': int(num_customers * 0.3),
        'assets': int(num_customers * 0.5),
        'tickets': int(num_customers * 1),
        'projects': int(num_customers * 0.05),
        'users': int(num_customers * 0.8),
        'inventory': int(num_customers * 0.2),  # Added missing entry for inventory
        'product_shipper': int(num_customers * 0.2)  # Added missing entry for product_shipper
    }

    num_loops = input("Enter the number of loops to run (default is endless): ").strip() or ''

    loop_count = 0
    while True:
        if num_loops and loop_count >= int(num_loops):
            break
        
        with ThreadPoolExecutor(max_workers=len(num_rows_dict)) as executor:
            futures = [executor.submit(create_and_populate_table, db_name, table_name, num_rows_dict[table_name]) 
                       for db_name, tables in databases.items() for table_name in tables]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error occurred: {e}")

        # Log run
        try:
            conn = mysql.connector.connect(**db_config_template)
            cursor = conn.cursor()
            conn.commit()
            logging.info("Run logged in MySQL log.")
        except mysql.connector.Error as err:
            logging.error(f"Logging error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        print("+------------------------------------------------------------------+")
        print("|   Loop completed. About to run again. Press Control-C to stop.   |")
        print("+------------------------------------------------------------------+")
        time.sleep(5)  # Wait before next run (adjust as needed)
        loop_count += 1

if __name__ == "__main__":
    main()