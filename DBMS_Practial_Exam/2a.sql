-- Create table: Student
CREATE TABLE Student (
    Roll INT PRIMARY KEY,
    Name VARCHAR(50),
    Address VARCHAR(100)
);

-- Create table: Subject
CREATE TABLE Subject (
    sub_code VARCHAR(10) PRIMARY KEY,
    sub_name VARCHAR(50)
);

-- Create table: Marks
CREATE TABLE Marks (
    Roll INT,
    sub_code VARCHAR(10),
    marks INT,
    FOREIGN KEY (Roll) REFERENCES Student(Roll),
    FOREIGN KEY (sub_code) REFERENCES Subject(sub_code)
);

-- Add new column  DOB into the table Student.
ALTER TABLE Student
ADD DOB DATE;

-- Modify the data types of any column.
ALTER TABLE Student
MODIFY Name VARCHAR(100);

-- Rename the column name sub_code to code.
ALTER TABLE Subject
RENAME COLUMN sub_code TO code;

-- Rename the table name Subject to Sub.
ALTER TABLE Subject
RENAME TO Sub;

-- Truncate the tables.
TRUNCATE TABLE Marks;
TRUNCATE TABLE Sub;
TRUNCATE TABLE Student;

-- Drop the tables.
DROP TABLE Marks;
DROP TABLE Sub;
DROP TABLE Student;


