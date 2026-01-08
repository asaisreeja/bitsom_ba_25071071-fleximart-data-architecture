# Database Schema Documentation – FlexiMart

---

## 1. Entity–Relationship Description

### 1.1 Entity: customers
**Purpose:** Stores customer information.

**Attributes:**
- customer_id: Unique identifier (Primary Key, Auto Increment)
- first_name: Customer’s first name
- last_name: Customer’s last name
- email: Unique email address
- phone: Contact number
- city: City of residence
- registration_date: Customer registration date

**Relationships:**
- One customer can place many orders (1:M relationship with orders table)

---

### 1.2 Entity: products
**Purpose:** Stores product catalog details.

**Attributes:**
- product_id: Unique identifier (Primary Key, Auto Increment)
- product_name: Name of the product
- category: Product category
- price: Price per unit
- stock_quantity: Available stock quantity

**Relationships:**
- One product can appear in many order_items (1:M relationship)

---

### 1.3 Entity: orders
**Purpose:** Stores customer order details.

**Attributes:**
- order_id: Unique identifier (Primary Key, Auto Increment)
- customer_id: Foreign key referencing customers.customer_id
- order_date: Date of order
- total_amount: Total value of the order
- status: Order status

**Relationships:**
- Many orders belong to one customer (M:1)
- One order can have many order_items (1:M)

---

### 1.4 Entity: order_items
**Purpose:** Stores item-level details for each order.

**Attributes:**
- order_item_id: Unique identifier (Primary Key, Auto Increment)
- order_id: Foreign key referencing orders.order_id
- product_id: Foreign key referencing products.product_id
- quantity: Quantity ordered
- unit_price: Price per unit
- subtotal: Calculated as quantity × unit_price

**Relationships:**
- Many order_items belong to one order
- Each order_item refers to one product

---

## 2. Normalization Explanation (Third Normal Form)

The database schema is designed in Third Normal Form (3NF) to reduce redundancy and ensure data integrity. Each table has a primary key, and all non-key attributes are fully functionally dependent on that primary key.

In the customers table, attributes such as first_name, last_name, email, city, and registration_date depend only on customer_id. There are no partial dependencies since the primary key consists of a single attribute.

The orders table stores only order-related information and references the customer using customer_id. Customer details are not duplicated in the orders table, preventing transitive dependencies. Similarly, the order_items table stores product references and pricing details without repeating product information such as product_name or category.

This design avoids update anomalies by ensuring that customer and product information is maintained in one place. Insert anomalies are avoided because customers and products can be added independently of orders. Delete anomalies are prevented because deleting an order does not remove customer or product records.

Thus, the schema satisfies all conditions of Third Normal Form.