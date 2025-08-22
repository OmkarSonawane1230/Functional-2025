#include <iostream>
#include <mysql_driver.h>
#include <mysql_connection.h>
#include <cppconn/prepared_statement.h>
using namespace sql;
using namespace std;

int main() {
    try {
        mysql::MySQL_Driver *driver =mysql::get_mysql_driver_instance();
        Connection *con = driver->connect("tcp://127.0.0.1:3306", "root", "mysql123");
        con->setSchema("Testing");

        PreparedStatement *pstmt = con->prepareStatement(
            "INSERT INTO Temp (id, name, login_status) VALUES (?, ?, ?)");
        pstmt->setInt(1, 4);
        pstmt->setString(2, "Diana");
        pstmt->setString(3, "Pending");
        pstmt->execute();

        cout << "Inserted into database.\n";
        delete pstmt;
        delete con;
    } catch (SQLException &e) {
        cerr << "SQL error: " << e.what() << endl;
    }
}