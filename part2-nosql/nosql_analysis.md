# NoSQL Justification Report – FlexiMart

## Section A: Limitations of RDBMS

Relational databases (MySQL, PostgreSQL) are widely used but have inherent limitations when dealing with highly diverse product catalogs like FlexiMart. The main limitations are:

- **Diverse Product Attributes:**  
  - Products in FlexiMart have very different attributes.  
  - Example: Laptops require fields like RAM, Processor, Storage; Shoes require Size, Color, Material.  
  - In a relational model, this requires either many nullable columns or multiple related tables, leading to complex schema design.

- **Frequent Schema Changes:**  
  - Adding new product types often requires altering table structures.  
  - Altering tables in production can be risky, time-consuming, and may cause downtime.  
  - This reduces flexibility and increases maintenance overhead.

- **Handling Nested Data (Customer Reviews):**  
  - Customer reviews need to be stored in separate tables linked via foreign keys.  
  - Fetching products with reviews requires multiple JOIN operations.  
  - This increases query complexity and can negatively affect performance as the dataset grows.
 
These limitations highlight that a rigid relational model may struggle to support a dynamic e-commerce environment with flexible product attributes and evolving requirements.

---

## Section B: Benefits of NoSQL (MongoDB)

MongoDB, a document-oriented NoSQL database, addresses the above limitations effectively:

- **Flexible Schema:**  
  - Each product document can have its own unique structure.  
  - No need to alter schema when introducing new product types.  
  - Perfect for a dynamic product catalog where attributes vary widely.

- **Embedded Documents for Nested Data:**  
  - Customer reviews can be embedded directly inside product documents.  
  - Allows retrieving product details along with reviews in a single query.  
  - Eliminates the need for multiple JOINs, improving query performance.

- **Horizontal Scalability:**  
  - MongoDB can scale across multiple servers using sharding.  
  - Efficiently handles large datasets and high traffic.  
  - Supports business growth without compromising performance.

- **Rapid Development and Flexibility:**  
  - Developers can iterate quickly without worrying about rigid table structures.  
  - Ideal for e-commerce platforms with rapidly changing business requirements.
 
Overall, MongoDB’s flexibility, scalability, and embedded document model make it suitable for managing FlexiMart’s diverse and evolving product catalog.


---

## Section C: Trade-offs of Using MongoDB

While MongoDB provides flexibility and scalability, it has some trade-offs:

- **Transaction Support Limitations:**  
  - Complex multi-document ACID transactions are more cumbersome than in relational databases.  
  - For strict financial or inventory operations, RDBMS may be safer.

- **Data Denormalization Risks:**  
  - MongoDB often duplicates data to improve query performance.  
  - Updates need careful handling to avoid inconsistencies.  
  - Can lead to potential update anomalies if not managed properly.

- **Query Limitations:**  
  - Aggregation and reporting may be less intuitive than SQL queries.  
  - Some complex analytics require additional processing or external tools.
 
- **Backup and Migration Considerations:**
  - Moving or restructuring large collections may be less intuitive than migrating normalized tables.
  - Planning and monitoring are crucial to avoid data loss.

---

### Summary

MongoDB is highly suitable for FlexiMart’s expanding product catalog because it allows:

1. Storage of diverse product attributes without schema changes.  
2. Embedding customer reviews for efficient retrieval.  
3. Horizontal scaling to support growth.  

However, careful consideration is required for transactions, data consistency, and complex queries.
