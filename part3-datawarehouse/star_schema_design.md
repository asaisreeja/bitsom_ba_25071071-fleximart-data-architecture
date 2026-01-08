# Task 3.1: Star Schema Design Documentation  
FlexiMart – Data Warehouse Design

---

## Section 1: Schema Overview (Star Schema)

This data warehouse uses a **Star Schema** to support efficient analytical reporting on historical sales data. The schema consists of one central fact table connected to multiple dimension tables.

---

## FACT TABLE: fact_sales

### Grain
- One row per **product per order line item**

### Business Process
- Sales transactions

### Measures (Numeric Facts)
- quantity_sold: Number of units sold  
- unit_price: Price per unit at the time of sale  
- discount_amount: Discount applied  
- total_amount: Final amount  
  - Formula: (quantity_sold × unit_price) − discount_amount

### Foreign Keys
- date_key → dim_date  
- product_key → dim_product  
- customer_key → dim_customer  

---

## DIMENSION TABLE: dim_date

### Purpose
- Supports time-based analysis (daily, monthly, quarterly, yearly)

### Type
- Conformed dimension

### Attributes
- date_key (PK): Surrogate key (YYYYMMDD)  
- full_date: Actual date  
- day_of_week: Monday, Tuesday, etc.  
- month: 1–12  
- month_name: January, February, etc.  
- quarter: Q1, Q2, Q3, Q4  
- year: 2023, 2024, etc.  
- is_weekend: Boolean  

---

## DIMENSION TABLE: dim_product

### Purpose
- Stores product-related descriptive data

### Attributes
- product_key (PK): Surrogate key  
- product_id: Source system product ID  
- product_name: Name of product  
- category: Electronics, Fashion, etc.  
- subcategory: Smartphones, Laptops, Clothing  
- brand: Manufacturer name  
- price_range: Budget, Mid-range, Premium  
- created_date: Product launch date  

---

## DIMENSION TABLE: dim_customer

### Purpose
- Enables customer-level analysis and segmentation

### Attributes
- customer_key (PK): Surrogate key  
- customer_id: Source system customer ID  
- customer_name: Full name  
- email: Customer email  
- city: City  
- state: State  
- country: Country  
- customer_segment: Regular, Premium, Wholesale  
- registration_date: Account creation date  

---

## Section 2: Design Decisions

The **transaction line-item level granularity** was selected to ensure detailed and flexible analysis. Each row represents a single product sold within an order, allowing the business to analyze sales performance at the lowest level and aggregate results as needed for reporting.

**Surrogate keys** are used instead of natural keys to improve performance and maintain data integrity. Natural keys may change over time or differ across systems, while surrogate keys remain stable and simplify joins between fact and dimension tables.

This design supports **drill-down** operations (year → quarter → month → day) and **roll-up** operations (product → category → total sales). The star schema structure reduces query complexity and improves performance, making it ideal for analytical workloads and business intelligence reporting.

---

## Section 3: Sample Data Flow

### Source Transaction
- Order ID: 101  
- Customer: John Doe  
- Product: Laptop  
- Quantity: 2  
- Unit Price: 50000  
- Order Date: 2024-01-15  

---

### Data Warehouse Representation

### fact_sales
- date_key: 20240115  
- product_key: 5  
- customer_key: 12  
- quantity_sold: 2  
- unit_price: 50000  
- discount_amount: 0  
- total_amount: 100000  

### dim_date
- date_key: 20240115  
- full_date: 2024-01-15  
- day_of_week: Monday  
- month: 1  
- month_name: January  
- quarter: Q1  
- year: 2024  
- is_weekend: false  

### dim_product
- product_key: 5  
- product_name: Laptop  
- category: Electronics  
- subcategory: Laptops  
- brand: Dell  
- price_range: Premium  

### dim_customer
- customer_key: 12  
- customer_name: John Doe  
- city: Mumbai  
- state: Maharashtra  
- country: India  
- customer_segment: Premium  

---

## Summary

This star schema design provides:
- Clear separation of facts and dimensions  
- High query performance  
- Easy scalability  
- Strong support for analytical reporting
