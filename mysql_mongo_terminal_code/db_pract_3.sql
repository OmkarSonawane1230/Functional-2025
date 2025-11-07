-- ✅ Use the database
USE CollegeDB;

-- ✅ Create Students Table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DOB DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    Email VARCHAR(100),
    DepartmentID INT,
    PhoneNumber VARCHAR(15)
);

-- ✅ Simple VIEW
CREATE VIEW StudentView AS
SELECT StudentID, FirstName, LastName
FROM Students;

-- ✅ INSERT Statements
INSERT INTO Students (StudentID, FirstName, LastName, DOB, Department)
VALUES 
(1, 'Omkar', 'Sonawane', '2005-12-30', 'Computer'),
(23, 'Prakash', 'Kumar', '2002-08-22', 'Mechanical'),
(3, 'Mohan', 'Shitole', '2004-02-01', 'Computer'),
(42, 'Ravi', 'Kharade', '2003-01-14', 'Civil'),
(3, 'Raviraj', 'Kharade', '2005-11-01', 'Mechanical'),
(16, 'Karan', 'Mane', '2004-05-21', 'Computer'),
(7, 'Raj', 'Sonawane', '2004-10-01', 'Electrical'),
(22, 'Prasad', 'Kakade', '2005-12-11', 'Auto Mobile'),
(34, 'Vishal', 'Sharma', '2005-09-11', 'Electrical');

-- ✅ SELECT with functions and operators

-- 1. Calculate Age using YEAR()
SELECT 
    StudentID,
    FirstName,
    LastName,
    YEAR(CURDATE()) - YEAR(DOB) AS Age
FROM Students;

-- 2. Logical Operators (AND, OR)
SELECT * FROM Students
WHERE DepartmentID = 1 AND Gender = 'Male';

-- 3. Arithmetic Operator
SELECT StudentID, FirstName, (StudentID + 100) AS UniqueID
FROM Students;

-- 4. String Function: UPPER
SELECT UPPER(FirstName) AS UpperName
FROM Students;

-- ✅ UPDATE Statement
-- Change phone number for Ravi Kumar
UPDATE Students
SET DOB = '2003-11-23'
WHERE FirstName = 'Ravi' AND LastName = 'Kharade';

-- ✅ DELETE Statement
-- Delete Simran's record
DELETE FROM Students
WHERE FirstName = 'Simran' AND LastName = 'Kaur';

-- ✅ SET OPERATORS

-- Create another temporary table for demo
CREATE TABLE Club_Members (
    StudentID INT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    ClubName VARCHAR(40)
);

-- Insert some overlapping and unique records
INSERT INTO Club_Members (StudentID, FirstName, LastName, ClubName)
VALUES
(1, 'Omkar', 'Sonawane', 'Sports'),
(23, 'Prakash', 'Kumar', 'Sports'),
(3, 'Mohan', 'Shitole', 'Coding'),
(12, 'Ravi', 'Kharade', 'Coding'),
(43, 'Vishnu', 'Shemane', 'Art Club'),
(24, 'Suraj', 'Shinde', 'Art Club');

-- 1. UNION - combines unique rows from both
SELECT FirstName, LastName FROM Students
UNION
SELECT FirstName, LastName FROM Club_Members;

-- 2. UNION ALL - includes duplicates
SELECT FirstName, LastName FROM Students
UNION ALL
SELECT FirstName, LastName FROM Club_Members;

-- 3. INTERSECT and MINUS are not supported in MySQL,
-- but you can simulate them using INNER JOIN and NOT IN / LEFT JOIN.

-- Simulate INTERSECT: common students
SELECT s.FirstName, s.LastName
FROM Students s
INNER JOIN Club_Members sa
ON s.FirstName = sa.FirstName AND s.LastName = sa.LastName;

-- Simulate MINUS: students in Students but not in Archive
SELECT FirstName, LastName FROM Students
WHERE (FirstName, LastName) NOT IN (
    SELECT FirstName, LastName FROM Club_Members
);
