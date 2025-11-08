"""
9_python.py

Requirements:
	pip install mysql-connector-python

To see the port number of your MySQL server, you can run the following SQL command:
    SHOW VARIABLES LIKE 'port';

"""

"""
Make sure that database and tables are created before running this program.

-- Create the database
CREATE DATABASE CollegeDB;

-- Use the database
USE CollegeDB;

-- Create a table for students
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    age INT,
    active BOOLEAN
);

INSERT INTO Students (student_id, name, department, age, active) VALUES
(1, 'Omkar Sonawane', 'Computer Engineering', 20, true),
(2, 'Raviraj Shingare', 'Civil Engineering', 19, false),
(3, 'Raj Sonawane', 'Computer Engineering', 21, true),
(4, 'Mahesh Salgar', 'Mechanical Engineering', 20, true);

SELECT * FROM Students;

"""

import mysql.connector
from mysql.connector import Error

def parse_bool(s: str) -> bool:
    return str(s).strip().lower() in ("true", "1", "yes", "y", "t")

def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid integer.")

def main():
    config = {
        "host": "localhost",
        "port": 3306,
        "database": "CollegeDB",
        "user": "root",
        "password": "mysql123",
    }

    conn = None
    try:
        conn = mysql.connector.connect(**config)
        if not conn.is_connected():
            print("Unable to connect to the database.")
            return

        while True:
            print("\n--- CollegeDB CRUD Menu ---")
            print("1. Add Student")
            print("2. View Students")
            print("3. Edit Student")
            print("4. Delete Student")
            print("5. Exit")
            try:
                choice = int(input("Enter your choice: ").strip())
            except ValueError:
                print("Invalid choice!")
                continue

            if choice == 1:
                student_id = get_int("Enter Student ID: ")
                name = input("Enter Name: ").strip()
                department = input("Enter Department: ").strip()
                age = get_int("Enter Age: ")
                active = parse_bool(input("Is Active (true/false): "))

                insert_sql = (
                    "INSERT INTO Students (student_id, name, department, age, active) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )
                cur = conn.cursor()
                try:
                    cur.execute(insert_sql, (student_id, name, department, age, active))
                    conn.commit()
                    print("Student added successfully!")
                except Error as e:
                    conn.rollback()
                    print("Error adding student:", e)
                finally:
                    cur.close()

            elif choice == 2:
                select_sql = "SELECT student_id, name, department, age, active FROM Students"
                cur = conn.cursor()
                try:
                    cur.execute(select_sql)
                    rows = cur.fetchall()
                    print("\nAll Students:")
                    for r in rows:
                        # r[4] may be 0/1 or boolean depending on connector; convert to bool for display
                        active_val = bool(r[4])
                        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {active_val}")
                except Error as e:
                    print("Error fetching students:", e)
                finally:
                    cur.close()

            elif choice == 3:
                edit_id = get_int("Enter Student ID to edit: ")
                new_name = input("Enter new Name: ").strip()
                new_dept = input("Enter new Department: ").strip()
                new_age = get_int("Enter new Age: ")
                new_active = parse_bool(input("Is Active (true/false): "))

                update_sql = (
                    "UPDATE Students SET name=%s, department=%s, age=%s, active=%s "
                    "WHERE student_id=%s"
                )
                cur = conn.cursor()
                try:
                    cur.execute(update_sql, (new_name, new_dept, new_age, new_active, edit_id))
                    conn.commit()
                    if cur.rowcount:
                        print("Student updated successfully!")
                    else:
                        print("No student found with that ID.")
                except Error as e:
                    conn.rollback()
                    print("Error updating student:", e)
                finally:
                    cur.close()

            elif choice == 4:
                del_id = get_int("Enter Student ID to delete: ")
                delete_sql = "DELETE FROM Students WHERE student_id=%s"
                cur = conn.cursor()
                try:
                    cur.execute(delete_sql, (del_id,))
                    conn.commit()
                    if cur.rowcount:
                        print("Student deleted successfully!")
                    else:
                        print("No student found with that ID.")
                except Error as e:
                    conn.rollback()
                    print("Error deleting student:", e)
                finally:
                    cur.close()

            elif choice == 5:
                print("Exiting...")
                break

            else:
                print("Invalid choice!")

    except Error as e:
        print("Database error:", e)
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()