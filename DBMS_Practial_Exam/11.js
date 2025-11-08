// This script demonstrates MongoDB aggregation and indexing
// Database: SalesDB
// Collection: Orders

// Use database
use SalesDB;

// Create Collection and Insert Documents
db.Orders.insertMany([
    { Order_ID: 1, Customer: "Ravi", City: "Delhi", Amount: 5000, Items: 5 },
    { Order_ID: 2, Customer: "Sneha", City: "Mumbai", Amount: 7000, Items: 7 },
    { Order_ID: 3, Customer: "Amit", City: "Delhi", Amount: 3000, Items: 3 },
    { Order_ID: 4, Customer: "Neha", City: "Chennai", Amount: 8000, Items: 8 },
    { Order_ID: 5, Customer: "Pratik", City: "Mumbai", Amount: 2000, Items: 2 }
]);

// Create an index on Customer and City fields to improve query performance
db.Orders.createIndex({ Customer: 1 });
db.Orders.createIndex({ City: 1, Amount: -1 });

// Aggregation Examples

// 1. Total sales amount for each city
db.Orders.aggregate([
    { $group: { _id: "$City", Total_Sales: { $sum: "$Amount" }, Total_Items: { $sum: "$Items" } } }
]);

// 2. Average order amount across all orders
db.Orders.aggregate([
    { $group: { _id: null, Average_Amount: { $avg: "$Amount" } } }
]);

// 3. Orders grouped by customer with total amount
db.Orders.aggregate([
    { $group: { _id: "$Customer", Total_Amount: { $sum: "$Amount" }, Total_Items: { $sum: "$Items" } } }
]);

// 4. Filter orders where Amount > 4000 and group by city
db.Orders.aggregate([
    { $match: { Amount: { $gt: 4000 } } },
    { $group: { _id: "$City", Total_Amount: { $sum: "$Amount" } } }
]);

// 5. Sort cities by total sales descending
db.Orders.aggregate([
    { $group: { _id: "$City", Total_Sales: { $sum: "$Amount" } } },
    { $sort: { Total_Sales: -1 } }
]);

// Display all orders to verify indexes and aggregation
db.Orders.find();
