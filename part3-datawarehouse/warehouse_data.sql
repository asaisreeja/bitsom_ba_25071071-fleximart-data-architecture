USE fleximart_dw;

--------------------------------------------------
-- INSERT INTO dim_date (30 dates: Jan–Feb 2024)
--------------------------------------------------

INSERT INTO dim_date VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,false),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,false),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,false),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,false),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,false),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,true),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,true),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,false),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,false),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,false),

(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,false),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,false),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,true),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,true),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,false),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,false),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,false),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,false),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,false),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,true);

--------------------------------------------------
-- INSERT INTO dim_product (15 products, 3 categories)
--------------------------------------------------

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001','Laptop Pro','Electronics','Laptops',85000),
('P002','Smartphone X','Electronics','Mobiles',45000),
('P003','Bluetooth Headphones','Electronics','Audio',5000),
('P004','4K Monitor','Electronics','Displays',32000),
('P005','Wireless Mouse','Electronics','Accessories',1200),

('P006','Running Shoes','Fashion','Footwear',6000),
('P007','Casual T-Shirt','Fashion','Clothing',1200),
('P008','Denim Jeans','Fashion','Clothing',2500),
('P009','Leather Jacket','Fashion','Outerwear',8500),
('P010','Sneakers','Fashion','Footwear',4000),

('P011','Office Chair','Furniture','Seating',12000),
('P012','Study Table','Furniture','Tables',15000),
('P013','Bookshelf','Furniture','Storage',8000),
('P014','Sofa Set','Furniture','Living Room',55000),
('P015','Bed Frame','Furniture','Bedroom',30000);

--------------------------------------------------
-- INSERT INTO dim_customer (12 customers, 4 cities)
--------------------------------------------------

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001','Rahul Sharma','Mumbai','Maharashtra','Premium'),
('C002','Anita Verma','Delhi','Delhi','Regular'),
('C003','Suresh Kumar','Bangalore','Karnataka','Regular'),
('C004','Pooja Singh','Chennai','Tamil Nadu','Premium'),
('C005','Amit Patel','Ahmedabad','Gujarat','Wholesale'),
('C006','Neha Gupta','Delhi','Delhi','Regular'),
('C007','Vikram Rao','Bangalore','Karnataka','Premium'),
('C008','Sneha Iyer','Chennai','Tamil Nadu','Regular'),
('C009','Rohan Mehta','Mumbai','Maharashtra','Wholesale'),
('C010','Kiran Das','Kolkata','West Bengal','Regular'),
('C011','Priya Nair','Kochi','Kerala','Premium'),
('C012','Arjun Malhotra','Delhi','Delhi','Regular');

--------------------------------------------------
-- INSERT INTO fact_sales (40 transactions)
--------------------------------------------------

INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount)
VALUES
(20240106,1,1,1,85000,5000,80000),
(20240107,2,2,2,45000,2000,88000),
(20240107,3,3,3,5000,0,15000),
(20240110,4,4,1,32000,2000,30000),
(20240110,5,5,4,1200,0,4800),

(20240203,6,6,2,6000,500,11500),
(20240203,7,7,3,1200,0,3600),
(20240204,8,8,2,2500,0,5000),
(20240204,9,9,1,8500,500,8000),
(20240205,10,10,2,4000,0,8000),

(20240206,11,11,1,12000,1000,11000),
(20240207,12,12,1,15000,0,15000),
(20240208,13,1,2,8000,1000,15000),
(20240209,14,2,1,55000,5000,50000),
(20240210,15,3,1,30000,0,30000),

(20240106,2,4,1,45000,0,45000),
(20240107,3,5,2,5000,0,10000),
(20240107,4,6,1,32000,2000,30000),
(20240108,5,7,3,1200,0,3600),
(20240109,6,8,1,6000,0,6000),

(20240201,7,9,2,1200,0,2400),
(20240202,8,10,1,2500,0,2500),
(20240203,9,11,1,8500,500,8000),
(20240203,10,12,2,4000,0,8000),
(20240204,11,1,1,12000,0,12000),

(20240205,12,2,1,15000,0,15000),
(20240206,13,3,2,8000,1000,15000),
(20240207,14,4,1,55000,5000,50000),
(20240208,15,5,1,30000,0,30000),
(20240209,1,6,1,85000,5000,80000),

(20240210,2,7,2,45000,2000,88000),
(20240210,3,8,3,5000,0,15000),
(20240204,4,9,1,32000,2000,30000),
(20240203,5,10,4,1200,0,4800),
(20240203,6,11,2,6000,500,11500);
