import java.sql.*;
import java.util.Scanner;

public class MySQL_DBNavigation {

    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/CollegeDB";   // Database URL
        String user = "root";                                   // MySQL username
        String password = "mysql123";                           // MySQL password

        try (Connection con = DriverManager.getConnection(url, user, password);
             Scanner sc = new Scanner(System.in)) {

            int choice;

            do {
                System.out.println("\n--- CollegeDB CRUD Menu ---");
                System.out.println("1. Add Student");
                System.out.println("2. View Students");
                System.out.println("3. Edit Student");
                System.out.println("4. Delete Student");
                System.out.println("5. Exit");
                System.out.print("Enter your choice: ");
                choice = sc.nextInt();
                sc.nextLine(); // consume newline

                switch (choice) {
                    case 1:
                        System.out.print("Enter Student ID: ");
                        int id = sc.nextInt(); sc.nextLine();
                        System.out.print("Enter Name: ");
                        String name = sc.nextLine();
                        System.out.print("Enter Department: ");
                        String dept = sc.nextLine();
                        System.out.print("Enter Age: ");
                        int age = sc.nextInt(); sc.nextLine();
                        System.out.print("Is Active (true/false): ");
                        boolean active = sc.nextBoolean(); sc.nextLine();

                        String insertSQL = "INSERT INTO Students (student_id, name, department, age, active) VALUES (?, ?, ?, ?, ?)";
                        try (PreparedStatement ps = con.prepareStatement(insertSQL)) {
                            ps.setInt(1, id);
                            ps.setString(2, name);
                            ps.setString(3, dept);
                            ps.setInt(4, age);
                            ps.setBoolean(5, active);
                            ps.executeUpdate();
                            System.out.println("Student added successfully!");
                        }
                        break;

                    case 2:
                        String selectSQL = "SELECT * FROM Students";
                        try (Statement stmt = con.createStatement();
                             ResultSet rs = stmt.executeQuery(selectSQL)) {

                            System.out.println("\nAll Students:");
                            while (rs.next()) {
                                System.out.println(rs.getInt("student_id") + " | " +
                                        rs.getString("name") + " | " +
                                        rs.getString("department") + " | " +
                                        rs.getInt("age") + " | " +
                                        rs.getBoolean("active"));
                            }
                        }
                        break;

                    case 3:
                        System.out.print("Enter Student ID to edit: ");
                        int editId = sc.nextInt(); sc.nextLine();
                        System.out.print("Enter new Name: ");
                        String newName = sc.nextLine();
                        System.out.print("Enter new Department: ");
                        String newDept = sc.nextLine();
                        System.out.print("Enter new Age: ");
                        int newAge = sc.nextInt(); sc.nextLine();
                        System.out.print("Is Active (true/false): ");
                        boolean newActive = sc.nextBoolean(); sc.nextLine();

                        String updateSQL = "UPDATE Students SET name=?, department=?, age=?, active=? WHERE student_id=?";
                        try (PreparedStatement ps = con.prepareStatement(updateSQL)) {
                            ps.setString(1, newName);
                            ps.setString(2, newDept);
                            ps.setInt(3, newAge);
                            ps.setBoolean(4, newActive);
                            ps.setInt(5, editId);
                            ps.executeUpdate();
                            System.out.println("Student updated successfully!");
                        }
                        break;

                    case 4:
                        System.out.print("Enter Student ID to delete: ");
                        int delId = sc.nextInt(); sc.nextLine();
                        String deleteSQL = "DELETE FROM Students WHERE student_id=?";
                        try (PreparedStatement ps = con.prepareStatement(deleteSQL)) {
                            ps.setInt(1, delId);
                            ps.executeUpdate();
                            System.out.println("Student deleted successfully!");
                        }
                        break;

                    case 5:
                        System.out.println("Exiting...");
                        break;

                    default:
                        System.out.println("Invalid choice!");
                }
            } while (choice != 5);

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
