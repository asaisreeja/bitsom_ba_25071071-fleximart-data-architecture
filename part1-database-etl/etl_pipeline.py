import pandas as pd
import re
from dateutil import parser
from datetime import datetime
import mysql.connector

print("ETL Pipeline started...")

# ============================================
# DATA QUALITY METRICS
# ============================================
report = []
report.append(f"ETL STARTED AT: {datetime.now()}")

# ============================================
# 1. EXTRACT DATA
# ============================================
customers = pd.read_csv("data\customers_raw.csv", sep=";")
products = pd.read_csv("data\products_raw.csv", sep=";")
sales = pd.read_csv("data\sales_raw.csv", sep=";")

print("Data extraction completed")
#print(customers.shape, products.shape, sales.shape)

report.append(f"Customers records read: {len(customers)}")
report.append(f"Products records read: {len(products)}")
report.append(f"Sales records read: {len(sales)}")


# ============================================
# HELPER FUNCTION
# ============================================

# Standardize phone

def standardize_phone(phone):
    if pd.isna(phone) or phone.strip() == "":
        return "+91-0000000000"
    phone = re.sub(r'\D', '', str(phone))  # remove non-digit chars
    if phone.startswith('0'):
        phone = phone[1:]
    if len(phone) > 10:
        phone = phone[-10:]  # keep last 10 digits
    if len(phone) < 10:
        return "+91-0000000000"
    return f"+91-{phone}"


# Standardize phone
#Convert date to YYYY-MM-DD format

def normalize_date(date_val):
    if pd.isna(date_val):
        return None

    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y","%m-%d-%Y"):
        try:
            return datetime.strptime(str(date_val), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None
customers["registration_date"] = customers["registration_date"].apply(normalize_date)


# ============================================
# 2. DATA CLEANING & TRANSFORMATION
# ============================================

# Customers Transformation

print("Started Data Cleaning and Transformation for customer data")
cust_dupes = customers.duplicated().sum()
# Remove duplicates

customers.drop_duplicates(subset="customer_id", inplace=True)

report.append(f"Customer duplicates removed: {cust_dupes}")

# Fill missing emails reliably
customers["email"] = customers["email"].fillna(
    "unknown_" + customers.index.to_series().astype(str) + "@mail.com"
)


# Standardize phone
   
customers["phone"] = customers["phone"].apply(standardize_phone)


# Normalize registration dates
customers["registration_date"] = pd.to_datetime(
    customers["registration_date"], errors='coerce'
)


#Save Cleaned Data 
customers.to_csv("customers_cleaned.csv", index=False)

print("Data Cleaning and Tranformation completed, Loaded the clean data to customers_cleaned.csv")


#-------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------

# Products Transformation

print("Started Data Cleaning and Transformation for products data")
prod_dupes = products.duplicated().sum()

# Clean column names
products.columns = products.columns.str.strip().str.lower()

# Remove duplicate rows and duplicate product IDs
products.drop_duplicates(inplace=True)
products.drop_duplicates(subset="product_id", inplace=True)

report.append(f"Product duplicates removed: {prod_dupes}")

# Handle missing values
products["price"] = products["price"].fillna(0.0)
products["stock_quantity"] = products["stock_quantity"].fillna(0)
products["category"] = products["category"].fillna("Unknown")

# Standardize category names (title case)
products["category"] = products["category"].str.strip().str.lower().str.title()


#Save Cleaned Data 
products.to_csv("products_cleaned.csv", index=False)

print("Data Cleaning and Transformation completed, Loaded the clean data to products_cleaned.csv")

#-------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------

print("Started Data Cleaning and Transformation for sales data")
sales_dupes = sales.duplicated().sum()

# Sales Transformation

sales.columns = sales.columns.str.strip().str.lower()

# -----------------------------
# Remove Duplicate Transactions
# -----------------------------
sales.drop_duplicates(inplace=True)

# -----------------------------
# Handle Missing Values
# -----------------------------
# Drop rows with missing customer_id or product_id
sales = sales.dropna(subset=["customer_id", "product_id","transaction_date"])

# Fill missing quantity with 1
sales["quantity"] = sales["quantity"].fillna(1).astype(int)

# Fill missing unit_price with 0.0
sales["unit_price"] = sales["unit_price"].fillna(0.0)

# Normalize dates
sales["transaction_date"] = sales["transaction_date"].apply(normalize_date)

# Calculate subtotal
sales["subtotal"] = sales["quantity"] * sales["unit_price"]


# -----------------------------
# Add Surrogate Keys
# -----------------------------
# Orders table: aggregate total_amount by customer + transaction_date
orders = sales.groupby(["customer_id", "transaction_date"]).agg(
    total_amount=pd.NamedAgg(column="subtotal", aggfunc="sum")
).reset_index()

orders["status"] = "Pending"  # Default status


# Build final order_items table
order_items = sales[["customer_id","product_id","quantity", "unit_price", "subtotal"]]

orders.to_csv("orders_cleaned.csv", index=False)

order_items.to_csv("order_items_cleaned.csv", index=False)

print("Data Cleaning and Transformation completed, Loaded the clean data to orders_cleaned.csv and order_items_cleaned.csv")
print("Data cleaning and transformation completed")
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")


#-------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------

# -----------------------------
# Database Connection
# -----------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",  # Replace with your MySQL password
        database="fleximart"
    )
    cursor = conn.cursor()
    print("Connected to MySQL database 'fleximart'")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Disable foreign key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

# Truncate tables in correct order
cursor.execute("TRUNCATE `fleximart`.`order_items`")
cursor.execute("TRUNCATE `fleximart`.`orders`")
cursor.execute("TRUNCATE `fleximart`.`customers`")
cursor.execute("TRUNCATE `fleximart`.`products`")


# -----------------------------
# Load Customers
# -----------------------------

customer_count=0

customer_id_map = {}

for _, row in customers.iterrows():
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row["first_name"],
        row["last_name"],
        row["email"],
        row["phone"],
        row["city"],
        row["registration_date"]
    ))
    customer_count +=1
    
    # Capture the MySQL auto-increment ID
    mysql_id = cursor.lastrowid
    customer_id_map[row["customer_id"]] = mysql_id  # Map CSV ID to MySQL ID

conn.commit()

print(f"Customers loaded successfully: {customer_count}")
report.append(f"Customers loaded successfully: {customer_count}")

# -----------------------------
# Load Products
# -----------------------------
product_count=0

products = pd.read_csv("products_cleaned.csv")
product_id_map = {}  # CSV product_id → MySQL product_id

for _, row in products.iterrows():
    cursor.execute("""
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (%s, %s, %s, %s)
    """, (
        row["product_name"],
        row["category"],
        row["price"],
        row["stock_quantity"]
    ))
    product_count +=1

    mysql_product_id = cursor.lastrowid
    product_id_map[row["product_id"]] = mysql_product_id
conn.commit()

print(f"Products loaded successfully: {product_count}")
report.append(f"Products loaded successfully: {product_count}")


# -----------------------------
# Load Orders
# -----------------------------

order_count=0

# Insert orders and capture MySQL order_ids

order_id_map = {}
for _, row in orders.iterrows():
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (%s, %s, %s, %s)
    """, (
        customer_id_map[row["customer_id"]],  # use mapped MySQL ID
        row["transaction_date"],
        row["total_amount"],
        row["status"]
    ))
    order_count += 1
    order_id_map[(row["customer_id"], row["transaction_date"])] = cursor.lastrowid

conn.commit()
print(f"Orders loaded successfully: {order_count}")
report.append(f"Orders loaded successfully: {order_count}")


# -----------------------------
# Load Order Items
# -----------------------------
item_count = 0
sales["order_id"] = sales.apply(
    lambda x: order_id_map.get((x["customer_id"], x["transaction_date"])),
    axis=1
)

for _, row in sales.iterrows():
    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row["order_id"],
        product_id_map[row["product_id"]],  # assuming product_id CSV matches MySQL products table
        row["quantity"],
        row["unit_price"],
        row["quantity"] * row["unit_price"]
    ))
    item_count += 1

conn.commit()
print(f"Order items loaded successfully: {item_count}")
report.append(f"Order items loaded successfully: {item_count}")
# Enable foreign key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# -----------------------------
# Commit & Close
# -----------------------------
conn.commit()
cursor.close()
conn.close()
print("All data loaded successfully into MySQL!")


#-------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------

# ============================================
#DATA QUALITY REPORT
# ============================================

report.append(f"ETL COMPLETED AT: {datetime.now()}")

with open("data_quality_report.txt", "w") as f:
    for line in report:
        f.write(line + "\n")

print("Data quality report generated")