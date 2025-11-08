-- Create a Library table and a Library_Audit table
CREATE TABLE Library (
    Book_ID INT PRIMARY KEY,
    Book_Name VARCHAR(100),
    Author VARCHAR(50),
    Qty INT
);

CREATE TABLE Library_Audit (
    Audit_ID INT AUTO_INCREMENT PRIMARY KEY,
    Book_ID INT,
    Book_Name VARCHAR(100),
    Author VARCHAR(50),
    Qty INT,
    Action_Type VARCHAR(10),
    Action_Time DATETIME
);

-- Insert sample data
INSERT INTO Library VALUES
(1, 'Database Systems', 'Korth', 5),
(2, 'Operating Systems', 'Tanenbaum', 3),
(3, 'Java Programming', 'Schildt', 10);

-- Trigger BEFORE UPDATE: store old values
DELIMITER $$

CREATE TRIGGER trg_Before_Update_Library
BEFORE UPDATE ON Library
FOR EACH ROW
BEGIN
    INSERT INTO Library_Audit(Book_ID, Book_Name, Author, Qty, Action_Type, Action_Time)
    VALUES(OLD.Book_ID, OLD.Book_Name, OLD.Author, OLD.Qty, 'UPDATE', NOW());
END$$

-- Trigger BEFORE DELETE: store old values
CREATE TRIGGER trg_Before_Delete_Library
BEFORE DELETE ON Library
FOR EACH ROW
BEGIN
    INSERT INTO Library_Audit(Book_ID, Book_Name, Author, Qty, Action_Type, Action_Time)
    VALUES(OLD.Book_ID, OLD.Book_Name, OLD.Author, OLD.Qty, 'DELETE', NOW());
END$$

DELIMITER ;

-- Update a record
UPDATE Library SET Qty = 8 WHERE Book_ID = 1;

-- Delete a record
DELETE FROM Library WHERE Book_ID = 2;

-- View the audit trail
SELECT * FROM Library_Audit;
