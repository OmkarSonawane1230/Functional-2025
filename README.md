# Functional-2025


# 🗄️ MySQL Integration in Codespaces (Ubuntu) with Node.js, Python, Java, and C++

This project demonstrates how to set up and interact with a MySQL server inside a Linux/Codespaces environment using multiple languages: **Node.js**, **Python**, **Java**, and **C++**.

---

## 📦 Table of Contents

- [🔧 Setup MySQL Server](#-setup-mysql-server)
- [⚙️ CLI Access to MySQL](#-cli-access-to-mysql)
- [🟢 Node.js Integration](#-nodejs-integration)
- [🐍 Python Integration](#-python-integration)
- [☕ Java Integration](#-java-integration)
- [🧾 C++ Integration](#-c-integration)
- [🧪 Common Errors & Fixes](#-common-errors--fixes)
- [✅ Final Notes](#-final-notes)

---

## 🔧 Setup MySQL Server

Install and start MySQL server:

```bash
sudo apt update
sudo apt install mysql-server
sudo service mysql start
```

Expected output after `sudo service mysql start` : **Ignore the warning**

```bash
 * Starting MySQL database server mysqld
su: warning: cannot change directory to /nonexistent: No such file or directory
/opt/conda/bin/xz
```

Change password for root (optional if already set):

```bash
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mysql123';
FLUSH PRIVILEGES;
EXIT;
```

---

## ⚙️ CLI Access to MySQL

**Before Logging in start the server**
```bash
sudo service mysql start
```

Now Login using:

```bash
mysql -u root -p
```

If socket error occurs:
Fix permissions (if socket file is there but access is denied)
`Error (13)` indicates a permissions issue. You may fix that with:

```bash
sudo chown -R mysql:mysql /var/run/mysqld
sudo chmod 755 /var/run/mysqld
sudo service mysql restart
```

Create a database and table:

```sql
CREATE DATABASE Testing;
USE Testing;

CREATE TABLE Temp (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  login_status VARCHAR(255) DEFAULT 'MySQL CLI'
);
```

---

## 🟢 Node.js Integration

Install dependencies:

```bash
npm init -y
npm install mysql2
```

**JavaScript (`mysql_in_javascript.js`):**

```javascript
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'mysql123',
  database: 'Testing'
});

connection.connect((err) => {
  if (err) throw err;
  console.log("Connected!");

  const sql = "INSERT INTO Temp (id, name, login_status) VALUES (?, ?, ?)";
  const values = [1, 'Alice', 'Inserted Through Javascript (Node.js)'];

  connection.query(sql, values, (err, result) => {
    if (err) throw err;
    console.log("Row inserted:", result);
    connection.end();
  });
});
```

Run:

```bash
node mysql_in_javascript.js
```

---

## 🐍 Python Integration

Install:

```bash
pip install mysql-connector-python
```

**Python (`mysql_in_python.py`):**

```python
import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql123",
  database="Testing"
)

cursor = conn.cursor()
cursor.execute("INSERT INTO Temp (id, name, login_status) VALUES (%s, %s, %s)", (2, "Bob", "Inserted Through Python"))
conn.commit()
print("Row inserted.")
cursor.close()
conn.close()
```

Run:

```bash
python3 mysql_in_python.py
```

---

## ☕ Java Integration (MySQL Connector/J 9.3.0)

**Step 1: Download the JDBC driver**

```bash
wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/9.3.0/mysql-connector-j-9.3.0.jar
```

**📝 Optional Improvement: Make It Reusable**

You can move the `.jar` file to a `lib/` folder and always reference it:
```bash
mkdir lib
mv mysql-connector-j-9.3.0.jar lib/
```

Then compile and run like:
```bash
javac -cp .:lib/mysql-connector-j-9.3.0.jar MySQLInJava.java
java -cp .:lib/mysql-connector-j-9.3.0.jar MySQLInJava
```

**Step 2: Java Code (`MySQLInJava.java`)**

```java
import java.sql.*;

public class MySQLInJava {
    public static void main(String[] args) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/Testing", "root", "mysql123");

            PreparedStatement stmt = conn.prepareStatement(
                "INSERT INTO Temp (id, name, login_status) VALUES (?, ?, ?)");
            stmt.setInt(1, 3);
            stmt.setString(2, "Charlie");
            stmt.setString(3, "Inserted Through Java");
            stmt.executeUpdate();

            System.out.println("Inserted successfully");
            stmt.close();
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**Step 3: Compile and Run**

```bash
javac -cp .:mysql-connector-j-9.3.0.jar MySQLInJava.java
java -cp .:mysql-connector-j-9.3.0.jar MySQLInJava
```

---

## 🧾 C++ Integration

Install MySQL Connector/C++:

```bash
sudo apt install libmysqlcppconn-dev -y
```

**C++ (`mysql_in_cpp.cpp`):**

```cpp
#include <iostream>
#include <mysql_driver.h>
#include <mysql_connection.h>
#include <cppconn/prepared_statement.h>

int main() {
    try {
        sql::mysql::MySQL_Driver *driver = sql::mysql::get_mysql_driver_instance();
        sql::Connection *con = driver->connect("tcp://127.0.0.1:3306", "root", "mysql123");
        con->setSchema("Testing");

        sql::PreparedStatement *pstmt = con->prepareStatement(
            "INSERT INTO Temp (id, name, login_status) VALUES (?, ?, ?)");
        pstmt->setInt(1, 4);
        pstmt->setString(2, "Diana");
        pstmt->setString(3, "Inserted Through C++");
        pstmt->execute();

        std::cout << "Inserted into database.\n";
        delete pstmt;
        delete con;
    } catch (sql::SQLException &e) {
        std::cerr << "SQL error: " << e.what() << std::endl;
    }
}
```

Compile & Run:

```bash
g++ -o mysql_in_cpp mysql_in_cpp.cpp -lmysqlcppconn
./mysql_in_cpp
```

---

## 🧪 Common Errors & Fixes

| ❌ Error | ✅ Fix |
|----------|--------|
| `MODULE_NOT_FOUND: 'mysql2'` in Node.js | Run `npm install mysql2` |
| Can't connect to local MySQL server through socket | Use `-h 127.0.0.1` when connecting |
| No suitable driver found for `jdbc:mysql://...` | Ensure MySQL JDBC `.jar` is in your classpath |
| Duplicate entry for PRIMARY KEY | Use a different id, or delete existing row |
| `ER_NOT_SUPPORTED_AUTH_MODE` | Run: <br>```sql<br>ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mysql123';```<br>```FLUSH PRIVILEGES;```<br> |

---