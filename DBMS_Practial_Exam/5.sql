-- Create tables for reference
CREATE TABLE Borrower (
    Roll INT,
    Name VARCHAR(50),
    DateofIssue DATE,
    NameofBook VARCHAR(100),
    Status CHAR(1)
);

CREATE TABLE Fine (
    Roll INT,
    Date DATE,
    Amt DECIMAL(10,2)
);

-- Sample data (you can modify as needed)
INSERT INTO Borrower VALUES
(1, 'Ravi', '2025-10-01', 'DBMS', 'I'),
(2, 'Sneha', '2025-09-15', 'Java', 'I'),
(3, 'Amit', '2025-11-01', 'Python', 'I');

-- ---------------------------------------------------------------
-- Stored Procedure: Calculate Fine and Update Status
-- ---------------------------------------------------------------
DELIMITER $

CREATE PROCEDURE ReturnBook(
    IN p_roll INT,
    IN p_book VARCHAR(100)
)
BEGIN
    DECLARE v_issue_date DATE;
    DECLARE v_days INT DEFAULT 0;
    DECLARE v_fine DECIMAL(10,2) DEFAULT 0;
    DECLARE not_found CONDITION FOR SQLSTATE '02000';

    -- Exception handler
    DECLARE EXIT HANDLER FOR not_found 
    BEGIN
        SELECT 'No record found for given Roll or Book' AS Message;
    END;

    -- Fetch issue date
    SELECT DateofIssue INTO v_issue_date
    FROM Borrower
    WHERE Roll = p_roll AND NameofBook = p_book AND Status = 'I';

    -- Calculate number of days since issue
    SET v_days = DATEDIFF(CURDATE(), v_issue_date);

    -- Fine calculation logic
    IF v_days > 30 THEN
        SET v_fine = v_days * 50;
    ELSEIF v_days >= 15 AND v_days <= 30 THEN
        SET v_fine = v_days * 5;
    ELSE
        SET v_fine = 0;
    END IF;

    -- Update status to 'R' (Returned)
    UPDATE Borrower
    SET Status = 'R'
    WHERE Roll = p_roll AND NameofBook = p_book;

    -- Insert into Fine table if fine applicable
    IF v_fine > 0 THEN
        INSERT INTO Fine (Roll, Date, Amt)
        VALUES (p_roll, CURDATE(), v_fine);
    END IF;

    -- Display results
    SELECT CONCAT('Book Returned Successfully! Days: ', v_days, ', Fine: Rs. ', v_fine) AS Message;
END$

DELIMITER ;

-- ---------------------------------------------------------------
-- Execute / Test the procedure
-- ---------------------------------------------------------------
CALL ReturnBook(1, 'DBMS');