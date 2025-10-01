import com.mongodb.client.*;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;
import org.bson.Document;

import java.util.Scanner;

public class MongoDBNavigation {

    public static void main(String[] args) {
        // Connect to MongoDB (local Docker container or server)
        MongoClient mongoClient = MongoClients.create("mongodb://root:example@localhost:27017");

        // Use database "mydb"
        MongoDatabase database = mongoClient.getDatabase("mydb");

        // Use collection "customers"
        MongoCollection<Document> collection = database.getCollection("customers");

        Scanner sc = new Scanner(System.in);
        int choice;

        do {
            System.out.println("\n--- MongoDB CRUD Menu ---");
            System.out.println("1. Add Customer");
            System.out.println("2. View Customers");
            System.out.println("3. Edit Customer");
            System.out.println("4. Delete Customer");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");
            choice = sc.nextInt();
            sc.nextLine(); // consume newline

            switch (choice) {
                case 1:
                    System.out.print("Enter Customer ID: ");
                    int id = sc.nextInt(); sc.nextLine();
                    System.out.print("Enter Name: ");
                    String name = sc.nextLine();
                    System.out.print("Enter City: ");
                    String city = sc.nextLine();
                    System.out.print("Enter Age: ");
                    int age = sc.nextInt(); sc.nextLine();
                    System.out.print("Is Active (true/false): ");
                    boolean active = sc.nextBoolean(); sc.nextLine();

                    Document doc = new Document("_id", id)
                            .append("name", name)
                            .append("city", city)
                            .append("age", age)
                            .append("active", active);

                    collection.insertOne(doc);
                    System.out.println("Customer added successfully!");
                    break;

                case 2:
                    System.out.println("\nAll Customers:");
                    FindIterable<Document> customers = collection.find();
                    for (Document customer : customers) {
                        System.out.println(customer.toJson());
                    }
                    break;

                case 3:
                    System.out.print("Enter Customer ID to edit: ");
                    int editId = sc.nextInt(); sc.nextLine();

                    System.out.print("Enter new Name: ");
                    String newName = sc.nextLine();
                    System.out.print("Enter new City: ");
                    String newCity = sc.nextLine();
                    System.out.print("Enter new Age: ");
                    int newAge = sc.nextInt(); sc.nextLine();
                    System.out.print("Is Active (true/false): ");
                    boolean newActive = sc.nextBoolean(); sc.nextLine();

                    collection.updateOne(
                            Filters.eq("_id", editId),
                            Updates.combine(
                                    Updates.set("name", newName),
                                    Updates.set("city", newCity),
                                    Updates.set("age", newAge),
                                    Updates.set("active", newActive)
                            )
                    );
                    System.out.println("Customer updated successfully!");
                    break;

                case 4:
                    System.out.print("Enter Customer ID to delete: ");
                    int delId = sc.nextInt(); sc.nextLine();
                    collection.deleteOne(Filters.eq("_id", delId));
                    System.out.println("Customer deleted successfully!");
                    break;

                case 5:
                    System.out.println("Exiting...");
                    break;

                default:
                    System.out.println("Invalid choice!");
            }
        } while (choice != 5);

        mongoClient.close();
        sc.close();
    }
}
