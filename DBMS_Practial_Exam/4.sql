-- Create Table: Salesman
CREATE TABLE Salesman (
    Salesman_id INT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50),
    commission DECIMAL(5,2)
);

-- Create Table: Customers
CREATE TABLE Customers (
    Customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    city VARCHAR(50),
    grade INT,
    Salesman_id INT,
    FOREIGN KEY (Salesman_id) REFERENCES Salesman(Salesman_id)
);

-- Create Table: Orders
CREATE TABLE Orders (
    ord_no INT PRIMARY KEY,
    ord_date DATE,
    purch_amt DECIMAL(10,2),
    Customer_id INT,
    Salesman_id INT,
    FOREIGN KEY (Customer_id) REFERENCES Customers(Customer_id),
    FOREIGN KEY (Salesman_id) REFERENCES Salesman(Salesman_id)
);

-- Insert Data into Salesman
INSERT INTO Salesman VALUES
(5001, 'James', 'London', 0.15),
(5002, 'Nail', 'Paris', 0.13),
(5005, 'Pit', 'Rome', 0.11),
(5006, 'Mc Lyon', 'Paris', 0.14),
(5007, 'Paul', 'Rome', 0.12);

-- Insert Data into Customers
INSERT INTO Customers VALUES
(3001, 'Brad', 'London', 2, 5001),
(3002, 'Nick', 'Paris', 3, 5002),
(3003, 'Rahul', 'Rome', 1, 5005),
(3004, 'John', 'Paris', 2, 5006),
(3005, 'Sameer', 'Rome', 3, 5007),
(3006, 'Arjun', 'Delhi', 1, 5001);

-- Insert Data into Orders
INSERT INTO Orders VALUES
(7001, '2012-10-05', 1500.00, 3001, 5001),
(7002, '2012-10-10', 2500.00, 3002, 5002),
(7003, '2012-10-10', 2000.00, 3003, 5005),
(7004, '2012-10-10', 1800.00, 3004, 5006),
(7005, '2012-10-12', 3000.00, 3005, 5007),
(7006, '2012-10-15', 2200.00, 3006, 5001);

-- 1. Find the name and city of those customers and salesmen who live in the same city
SELECT c.customer_name, c.city, s.name AS salesman_name
FROM Customers c
JOIN Salesman s ON c.city = s.city;

-- 2. Find the names of all customers along with the salesmen who work for them
SELECT c.customer_name, s.name AS salesman_name
FROM Customers c
JOIN Salesman s ON c.Salesman_id = s.Salesman_id;

-- 3. Display all those orders by customers not located in the same city as their salesmen
SELECT o.ord_no, o.purch_amt, c.customer_name, c.city AS customer_city, s.city AS salesman_city
FROM Orders o
JOIN Customers c ON o.Customer_id = c.Customer_id
JOIN Salesman s ON o.Salesman_id = s.Salesman_id
WHERE c.city <> s.city;

-- 4. Display all the orders whose values are greater than the average order value for 10th October 2012
SELECT * 
FROM Orders
WHERE purch_amt > (
    SELECT AVG(purch_amt)
    FROM Orders
    WHERE ord_date = '2012-10-10'
);

-- 5. Find all orders attributed to salesmen in Paris
SELECT o.ord_no, o.ord_date, o.purch_amt, s.name AS salesman_name, s.city
FROM Orders o
JOIN Salesman s ON o.Salesman_id = s.Salesman_id
WHERE s.city = 'Paris';
