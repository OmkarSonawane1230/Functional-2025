CREATE TABLE Library (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(100),
    Author VARCHAR(100),
    Published_Year INT
);


CREATE TABLE Library_Audit (
    AID INT PRIMARY KEY AUTO_INCREMENT,
    BID INT,
    Title VARCHAR(60),
    Op VARCHAR(10),
    OpTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO Library (Title, Author, Published_Year) VALUES
('Database Systems', 'C. J. Date', 2019),
('Learning SQL', 'Alan Beaulieu', 2020),
('PL/SQL Programming', 'Steven Feuerstein', 2018),
('Wings of Fire', 'A. P. J. Abdul Kalam', 1999),
('The Guide', 'R. K. Narayan', 1958),
('Train to Pakistan', 'Khushwant Singh', 1956),
('Clean Code', 'Robert C. Martin', 2008),
('Design Patterns', 'Erich Gamma', 1994),
('Introduction to Algorithms', 'Thomas H. Cormen', 2009),
('Effective Java', 'Joshua Bloch', 2017),
('The Pragmatic Programmer', 'Andrew Hunt', 1999),
('India After Gandhi', 'Ramachandra Guha', 2007),
('The White Tiger', 'Aravind Adiga', 2008);


-- Trigger for udpate

DELIMITER $

CREATE TRIGGER trg_Library_Update
AFTER UPDATE ON Library
FOR EACH ROW
BEGIN
    INSERT INTO Library_Audit(BID, Title, Op)
    VALUES (OLD.BookID, OLD.Title, 'UPDATE');
END $


-- Trigger for delete

DELIMITER $

CREATE TRIGGER trg_Library_Delete
AFTER DELETE ON Library
FOR EACH ROW
BEGIN
    INSERT INTO Library_Audit(BID, Title, Op)
    VALUES (OLD.BookID, OLD.Title, 'DELETE');
END $


-- Update by Suresh
UPDATE Library SET Published_Year = 2005 WHERE BookID = 9;

-- Delete by Amit
DELETE FROM Library WHERE BookID = 2;$

-- Delete by Kiran
DELETE FROM Library WHERE BookID = 7;$
