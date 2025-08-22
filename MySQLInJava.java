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