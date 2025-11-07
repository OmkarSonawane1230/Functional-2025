-- ✅ USE DATABASE
USE CollegeDB;

-- ✅ TABLES USED:
-- Student(StudentID, FirstName, LastName, DOB, Email, Department)
-- Club_Members(StudentID, FirstName, LastName, ClubName)

-- ---------------------------------------------------
-- ✅ 1. JOINS
-- ---------------------------------------------------

-- INNER JOIN: Students who are in a club
SELECT s.StudentID, s.FirstName, s.LastName, s.Department, c.ClubName
FROM Students s
INNER JOIN Club_Members c ON s.StudentID = c.StudentID;

-- LEFT JOIN: All students, even those not in any club
SELECT s.StudentID, s.FirstName, s.LastName, c.ClubName
FROM Students s
LEFT JOIN Club_Members c ON s.StudentID = c.StudentID;

-- RIGHT JOIN: All club members, even if not found in Student table
SELECT s.StudentID, s.FirstName, s.LastName, c.ClubName
FROM Students s
RIGHT JOIN Club_Members c ON s.StudentID = c.StudentID;

-- CROSS JOIN:
SELECT s.StudentID, s.FirstName, s.LastName, c.ClubName
FROM Students s
CROSS JOIN Club_Members c ON s.StudentID = c.StudentID;

-- FULL OUTER JOIN (Simulated using UNION of LEFT and RIGHT JOIN)
SELECT s.StudentID, s.FirstName, s.LastName, c.ClubName
FROM Students s
LEFT JOIN Club_Members c ON s.StudentID = c.StudentID
UNION
SELECT s.StudentID, s.FirstName, s.LastName, c.ClubName
FROM Students s
RIGHT JOIN Club_Members c ON s.StudentID = c.StudentID;

-- ---------------------------------------------------
-- ✅ 2. SUBQUERIES
-- ---------------------------------------------------

-- Single-row subquery: Find student with oldest DOB
SELECT * FROM Students
WHERE DOB = (
    SELECT MIN(DOB) FROM Students
);

-- Multi-row subquery: Students in departments 'Science' or 'Arts'
SELECT * FROM Students
WHERE Department IN (
    SELECT DISTINCT Department FROM Students
    WHERE Department IN ('Science', 'Arts')
);

-- Correlated subquery: Find students who share their first name with someone in Club_Members
SELECT s.StudentID, s.FirstName
FROM Students s
WHERE EXISTS (
    SELECT 1 FROM Club_Members c
    WHERE c.FirstName = s.FirstName
);

-- ---------------------------------------------------
-- ✅ 3. VIEWS
-- ---------------------------------------------------

-- View of Student basic info
CREATE VIEW BasicStudentView AS
SELECT StudentID, FirstName, LastName, Department
FROM Students;

-- View of students with their club names (only those in a club)
CREATE VIEW StudentClubView AS
SELECT s.StudentID, s.FirstName, s.LastName, c.ClubName
FROM Students s
JOIN Club_Members c ON s.StudentID = c.StudentID;

-- View usage examples
SELECT * FROM BasicStudentView;
SELECT * FROM StudentsClubView;

-- ✅ End of File
