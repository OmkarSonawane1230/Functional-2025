-- 1. Insert minimum 5 values in all tables

INSERT INTO Student (Roll, Name, Address) VALUES
(1, 'Pratik', 'Pune'),
(2, 'Aditi', 'Mumbai'),
(3, 'Rohan', 'Nagpur'),
(4, 'Sneha', 'Nashik'),
(5, 'Karan', 'Kolhapur');

INSERT INTO Subject (sub_code, sub_name) VALUES
('DBMS', 'Database Management System'),
('DMS', 'Discrete Mathematics'),
('OS', 'Operating System'),
('CN', 'Computer Networks'),
('JAVA', 'Java Programming');

INSERT INTO Marks (Roll, sub_code, marks) VALUES
(1, 'DBMS', 85),
(2, 'DMS', 60),
(3, 'OS', 72),
(4, 'CN', 90),
(5, 'JAVA', 65);

-- 2. Update row where the value of sub_code = 'DMS'
UPDATE Subject
SET sub_name = 'Discrete Mathematics Structure'
WHERE sub_code = 'DMS';

-- 3. Find the students whose marks are less than 75
SELECT s.Roll, s.Name, s.Address, m.sub_code, m.marks
FROM Student s
JOIN Marks m ON s.Roll = m.Roll
WHERE m.marks < 75;

-- 4. Delete the record of the student whose name = 'Pratik'
DELETE FROM Student
WHERE Name = 'Pratik';