INSERT INTO Cust_New (CustID, CustName, City) VALUES
(2, 'Suresh Patil', 'Mumbai'),
(3, 'Anita Desai', 'Pune'),
(4, 'Vikram Singh', 'Delhi'),
(5, 'Priya Iyer', 'Chennai'),
(6, 'Rahul Mehta', 'Pune');


DELIMITER $

CREATE PROCEDURE Merge_Customers_ByCity(IN city_param VARCHAR(50))
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE v_city VARCHAR(50);
    DECLARE done INT DEFAULT 0;

    -- Cursor: fetch customers from Cust_New for the given city
    DECLARE cur CURSOR FOR 
        SELECT CustID, CustName, City 
        FROM Cust_New 
        WHERE City = city_param;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_id, v_name, v_city;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;

        -- Insert only if not exists in Cust_Old
        IF NOT EXISTS (SELECT 1 FROM Cust_Old WHERE CustID = v_id) THEN
            INSERT INTO Cust_Old (CustID, CustName, City) 
            VALUES (v_id, v_name, v_city);
        END IF;
    END LOOP;

    CLOSE cur;
END $