-- 1. Create Tables
CREATE TABLE Student (
    Roll INT PRIMARY KEY,
    Name VARCHAR(50),
    Address VARCHAR(100)
);

CREATE TABLE Subject (
    sub_code VARCHAR(10) PRIMARY KEY,
    sub_name VARCHAR(50)
);

CREATE TABLE Marks (
    Roll INT,
    sub_code VARCHAR(10),
    marks INT,
    FOREIGN KEY (Roll) REFERENCES Student(Roll),
    FOREIGN KEY (sub_code) REFERENCES Subject(sub_code)
);

-- 2. Create View on Subject
CREATE VIEW view_subject AS
SELECT sub_code, sub_name
FROM Subject;

-- 3. Create Index on Marks with sub_code
CREATE INDEX idx_subcode ON Marks(sub_code);
