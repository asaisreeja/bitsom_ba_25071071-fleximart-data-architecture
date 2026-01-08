/*****************************************************
 OPERATION 1: Load Data
*****************************************************/

// Directly imported data into Mongo db into Database called Sreeja and collection products , below is the output

// Switch to the required database

// use Sreeja;     mongosh Sreeja mongodb_operations.js     - ran this command which succefully generated the ouput


// Count total documents to confirm successful import

db.products.countDocuments();

// Expected Output:
// 12

print("Operation 1 completed: Data loaded and verified");


/*****************************************************
 OPERATION 2: Basic Query
*****************************************************/

/*
Objective:
Retrieve all Electronics products
where price is less than 50,000.

Only display product name, price, and stock.
*/

// Execute find query with filter and projection
db.products.find(
  {
    category: "Electronics",        // Filter by category
    price: { $lt: 50000 }           // Price condition
  },
  {
    _id: 0,                         // Exclude MongoDB ID
    name: 1,                        // Include product name
    price: 1,                       // Include price
    stock: 1                        // Include stock
  }
);

print("Operation 2 completed: Basic query executed");


/*****************************************************
 OPERATION 3: Review Analysis
*****************************************************/

/*
Objective:
Identify products having average rating >= 4.0.

Steps:
1. Unwind reviews array
2. Calculate average rating per product
3. Filter products based on average rating
4. Format final output
*/

db.products.aggregate([
  
  // Convert reviews array into individual documents
  { $unwind: "$reviews" },

  // Group reviews by product name and calculate average rating
  {
    $group: {
      _id: "$name",
      avg_rating: { $avg: "$reviews.rating" }
    }
  },

  // Filter products with average rating >= 4.0
  {
    $match: {
      avg_rating: { $gte: 4.0 }
    }
  },

  // Format final output
  {
    $project: {
      _id: 0,
      product_name: "$_id",
      avg_rating: { $round: ["$avg_rating", 2] }
    }
  }
]);

print("Operation 3 completed: Review analysis done");


/*****************************************************
 OPERATION 4: Update Operation
*****************************************************/

/*
Objective:
Add a new customer review to an existing product
with product_id = "ELEC001".

Demonstrates:
- Embedded documents
- Update using $push
*/

db.products.updateOne(
  
  // Match the product
  { product_id: "ELEC001" },

  // Push new review into reviews array
  {
    $push: {
      reviews: {
        user_id: "U999",
        rating: 4,
        comment: "Good value",
        date: new Date()
      }
    }
  }
);

print("Operation 4 completed: Review added successfully");


/*****************************************************
 OPERATION 5: Complex Aggregation
*****************************************************/

/*
Objective:
Perform category-wise analysis to find:
- Average price of products
- Total product count per category

Results should be sorted by average price (descending).
*/

db.products.aggregate([

  // Group products by category
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },

  // Rename fields and format output
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: { $round: ["$avg_price", 2] },
      product_count: 1
    }
  },

  // Sort categories by average price
  {
    $sort: { avg_price: -1 }
  }
]);

print("Operation 5 completed: Aggregation successful");


/*****************************************************
 END OF FILE
*****************************************************/

print("All MongoDB operations executed successfully");
