-- Create tables Stud_Marks and Result
CREATE TABLE Stud_Marks (
    Roll INT PRIMARY KEY,
    Name VARCHAR(50),
    Total_Marks INT
);

CREATE TABLE Result (
    Roll INT,
    Name VARCHAR(50),
    Class VARCHAR(30)
);

-- Insert sample student data
INSERT INTO Stud_Marks VALUES
(1, 'Ravi', 1450),
(2, 'Sneha', 940),
(3, 'Amit', 870),
(4, 'Neha', 760);


-- Stored procedure proc_Grade to categorize students based on total marks
DELIMITER $$

CREATE PROCEDURE proc_Grade(IN p_roll INT)
BEGIN
    DECLARE v_name VARCHAR(50);
    DECLARE v_marks INT;
    DECLARE v_class VARCHAR(30);
    DECLARE not_found CONDITION FOR SQLSTATE '02000';

    DECLARE EXIT HANDLER FOR not_found 
    BEGIN
        SELECT CONCAT('No record found for Roll = ', p_roll) AS Message;
    END;

    SELECT Name, Total_Marks 
    INTO v_name, v_marks
    FROM Stud_Marks
    WHERE Roll = p_roll;

    IF v_marks BETWEEN 990 AND 1500 THEN
        SET v_class = 'Distinction';
    ELSEIF v_marks BETWEEN 900 AND 989 THEN
        SET v_class = 'First Class';
    ELSEIF v_marks BETWEEN 825 AND 899 THEN
        SET v_class = 'Higher Second Class';
    ELSE
        SET v_class = 'Fail';
    END IF;

    INSERT INTO Result (Roll, Name, Class)
    VALUES (p_roll, v_name, v_class);

    SELECT CONCAT('Result recorded for ', v_name, ' → ', v_class) AS Message;
END$$

DELIMITER ;

-- Calls the procedure for all students
CALL proc_Grade(1);
CALL proc_Grade(2);
CALL proc_Grade(3);
CALL proc_Grade(4);

-- Displays the Result table

SELECT * FROM Result;
