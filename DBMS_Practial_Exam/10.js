// Use database
use LibraryDB;

// Create Collection and Insert Documents
db.Students.insertMany([
    { Roll: 1, Name: "Ravi", Address: "Delhi", Age: 20, Marks: 85 },
    { Roll: 2, Name: "Sneha", Address: "Mumbai", Age: 22, Marks: 92 },
    { Roll: 3, Name: "Amit", Address: "Bangalore", Age: 21, Marks: 78 },
    { Roll: 4, Name: "Neha", Address: "Chennai", Age: 23, Marks: 65 },
    { Roll: 5, Name: "Pratik", Address: "Delhi", Age: 20, Marks: 55 }
]);

// Read/Find Documents

// Find all students
db.Students.find();

// Find student with Roll = 2
db.Students.find({ Roll: 2 });

// Find students with Marks greater than 80
db.Students.find({ Marks: { $gt: 80 } });

// Find students with Age between 20 and 22 using logical operator
db.Students.find({ $and: [{ Age: { $gte: 20 } }, { Age: { $lte: 22 } }] });

// Find students whose Address is either Delhi or Mumbai using $or
db.Students.find({ $or: [{ Address: "Delhi" }, { Address: "Mumbai" }] });

// Update Documents

// Update Marks of Roll = 1 to 90
db.Students.updateOne({ Roll: 1 }, { $set: { Marks: 90 } });

// Update multiple students: increase Marks by 5 for students in Delhi
db.Students.updateMany({ Address: "Delhi" }, { $inc: { Marks: 5 } });

// Save Method

// save() inserts a new document or updates if _id exists
db.Students.save({ Roll: 6, Name: "Aarav", Address: "Kolkata", Age: 24, Marks: 88 });

// Delete Documents

// Delete student with Roll = 5
db.Students.deleteOne({ Roll: 5 });

// Delete all students with Marks less than 60
db.Students.deleteMany({ Marks: { $lt: 60 } });

// Final View of Collection
db.Students.find();
