// This script demonstrates MongoDB MapReduce operation
// Database: SalesDB
// Collection: Orders

// Use database
use SalesDB;

// Create Collection and Insert Documents
db.Orders.insertMany([
    { Order_ID: 1, Customer: "Ravi", City: "Delhi", Amount: 5000 },
    { Order_ID: 2, Customer: "Sneha", City: "Mumbai", Amount: 7000 },
    { Order_ID: 3, Customer: "Amit", City: "Delhi", Amount: 3000 },
    { Order_ID: 4, Customer: "Neha", City: "Chennai", Amount: 8000 },
    { Order_ID: 5, Customer: "Pratik", City: "Mumbai", Amount: 2000 }
]);

// Map function: emits City as key and Amount as value
var mapFunction = function() {
    emit(this.City, this.Amount);
};

// Reduce function: sums all Amounts for each City
var reduceFunction = function(key, values) {
    return Array.sum(values);
};

// Execute MapReduce
db.Orders.mapReduce(
    mapFunction,
    reduceFunction,
    { out: "City_Total_Sales" } // Output collection
);

// Display the result
db.City_Total_Sales.find();
