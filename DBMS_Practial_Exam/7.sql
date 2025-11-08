-- Create two tables Cust_New and Cust_Old

CREATE TABLE Cust_Old (
    Customer_id INT PRIMARY KEY,
    Customer_name VARCHAR(50),
    City VARCHAR(50)
);

CREATE TABLE Cust_New (
    Customer_id INT PRIMARY KEY,
    Customer_name VARCHAR(50),
    City VARCHAR(50)
);

-- Insert sample data into Cust_Old
INSERT INTO Cust_Old VALUES
(1, 'Ravi', 'Delhi'),
(2, 'Sneha', 'Mumbai');

-- Insert sample data into Cust_New
INSERT INTO Cust_New VALUES
(2, 'Sneha', 'Mumbai'),
(3, 'Amit', 'Bangalore'),
(4, 'Neha', 'Chennai');


-- Stored procedure using a parameterized cursor
DELIMITER $$

CREATE PROCEDURE Merge_Customers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_cust_id INT;
    DECLARE v_cust_name VARCHAR(50);
    DECLARE v_city VARCHAR(50);

    -- Declare parameterized cursor
    DECLARE cur_new CURSOR FOR 
        SELECT Customer_id, Customer_name, City FROM Cust_New;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur_new;

    read_loop: LOOP
        FETCH cur_new INTO v_cust_id, v_cust_name, v_city;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Check if customer already exists in Cust_Old
        IF NOT EXISTS (SELECT 1 FROM Cust_Old WHERE Customer_id = v_cust_id) THEN
            INSERT INTO Cust_Old (Customer_id, Customer_name, City)
            VALUES (v_cust_id, v_cust_name, v_city);
        END IF;

    END LOOP;

    CLOSE cur_new;

    SELECT * FROM Cust_Old;
END$$

DELIMITER ;

-- Execute the procedure
CALL Merge_Customers();
