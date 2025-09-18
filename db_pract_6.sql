CREATE TABLE Stud_Marks (
    Roll INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Total_Marks INT
);

CREATE TABLE Result (
    Roll INT,
    Name VARCHAR(50),
    Class VARCHAR(30)
);

TRUNCATE TABLE Stud_Marks;

INSERT INTO Stud_Marks(Name, Total_Marks) VALUES
('Amit Sharma', 1200),
('Sita Rani', 980),
('Ramesh Kumar', 890),
('Geeta Joshi', 810),
('Vikas Patel', 1500),
('Priya Nair', 905),
('Anil Singh', 830),
('Meena Rao', 750),
('Rahul Verma', 999),
('Kiran Das', 910);


DELIMITER $

CREATE FUNCTION fn_Grade(marks INT)
RETURNS VARCHAR(30)
DETERMINISTIC
BEGIN
    DECLARE grade VARCHAR(30);

    IF marks BETWEEN 990 AND 1500 THEN
        SET grade = 'Distinction';
    ELSEIF marks BETWEEN 900 AND 989 THEN
        SET grade = 'First Class';
    ELSEIF marks BETWEEN 825 AND 899 THEN
        SET grade = 'Higher Second Class';
    ELSE
        SET grade = 'Fail';
    END IF;

    RETURN grade;
END $


DELIMITER $

CREATE PROCEDURE proc_Grade()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE vRoll INT;
    DECLARE vName VARCHAR(50);
    DECLARE vMarks INT;

    DECLARE cur CURSOR FOR 
        SELECT Roll, Name, Total_Marks FROM Stud_Marks;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO vRoll, vName, vMarks;
        IF done THEN
            LEAVE read_loop;
        END IF;

        INSERT INTO Result(Roll, Name, Class)
        VALUES(vRoll, vName, fn_Grade(vMarks));
    END LOOP;

    CLOSE cur;
END $

