-- 1. CREATE DATABASE and USE
CREATE DATABASE CollegeDB;
USE CollegeDB;

-- 2. CREATE TABLES

-- Student Table
CREATE TABLE Student (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DOB DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    Email VARCHAR(100),
    DepartmentID INT
);

-- Department Table
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
    DepartmentName VARCHAR(100)
);

-- Course Table
CREATE TABLE Course (
    CourseID INT PRIMARY KEY AUTO_INCREMENT,
    CourseName VARCHAR(100),
    DepartmentID INT
);

-- Enrollment Table (Many-to-Many)
CREATE TABLE Enrollment (
    EnrollmentID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    CourseID INT,
    EnrollmentDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

-- 3. ALTER TABLE
-- Add PhoneNumber column to Student table
ALTER TABLE Student ADD PhoneNumber VARCHAR(15);

-- 4. DROP TABLE
-- Drop the Enrollment table
DROP TABLE Enrollment;

-- 5. TRUNCATE TABLE
-- Truncate Course table
TRUNCATE TABLE Course;

-- 6. RENAME TABLE
-- Rename Student table to Students
RENAME TABLE Student TO Students;

-- 7. CREATE VIEW
-- View combining student and department info
CREATE VIEW StudentView AS
SELECT StudentID, FirstName, LastName
FROM Students;


-- 8. CREATE INDEX
-- Index on Email column in Students table
CREATE INDEX idx_email ON Students(Email);

-- 9. CREATE SEQUENCE (simulated using AUTO_INCREMENT)
-- Already used in table definitions
-- Alternatively, create a table with AUTO_INCREMENT
CREATE TABLE SequenceDemo (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Note VARCHAR(100)
);

-- 10. SYNONYM (MySQL does not support it)
-- Simulate using VIEW
CREATE VIEW StudentSynonym AS SELECT * FROM Students;

-- Or use alias in SELECT
-- SELECT * FROM Students AS S;
