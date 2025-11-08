-- Create the table to store radius and area
CREATE TABLE IF NOT EXISTS areas (
    radius INT,
    area DOUBLE
);

-- PL/SQL-style block in MySQL using procedural syntax
DELIMITER $$

CREATE PROCEDURE CalculateCircleAreas()
BEGIN
    DECLARE r INT DEFAULT 5;
    DECLARE a DOUBLE;
    
    -- Loop through radius values from 5 to 9
    WHILE r <= 9 DO
        -- Calculate area of the circle using PI() function
        SET a = PI() * r * r;
        
        -- Insert radius and area into the table
        INSERT INTO areas (radius, area) VALUES (r, a);
        
        -- Increment radius
        SET r = r + 1;
    END WHILE;
END$$

DELIMITER ;

-- Call the procedure to populate the table
CALL CalculateCircleAreas();

-- View the results
SELECT * FROM areas;
