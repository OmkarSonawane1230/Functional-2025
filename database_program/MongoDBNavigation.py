"""
MongoDBNavigation.py

Requirements:
	pip install pymongo
"""

from pymongo import MongoClient, errors


def input_int(prompt):
	while True:
		try:
			return int(input(prompt).strip())
		except ValueError:
			print("Please enter a valid integer.")


def input_bool(prompt):
	while True:
		val = input(prompt).strip().lower()
		if val in ("true", "t", "yes", "y", "1"):
			return True
		if val in ("false", "f", "no", "n", "0"):
			return False
		print("Please enter true/false (or yes/no).")


def main():
	# Connect to local MongoDB
	try:
		client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=3000)
		# Trigger server selection to raise early if not available
		client.server_info()
	except errors.ServerSelectionTimeoutError:
		print("Could not connect to MongoDB at mongodb://127.0.0.1:27017. Make sure MongoDB is running.")
		return

	db = client["mydb"]
	collection = db["users"]

	try:
		while True:
			print("\n--- MongoDB CRUD Menu ---")
			print("1. Add Customer")
			print("2. View Customers")
			print("3. Edit Customer")
			print("4. Delete Customer")
			print("5. Exit")
			choice = input_int("Enter your choice: ")

			if choice == 1:
				id_ = input_int("Enter Customer ID: ")
				name = input("Enter Name: ").strip()
				city = input("Enter City: ").strip()
				age = input_int("Enter Age: ")
				active = input_bool("Is Active (true/false): ")

				doc = {"_id": id_, "name": name, "city": city, "age": age, "active": active}
				try:
					collection.insert_one(doc)
					print("Customer added successfully!")
				except errors.DuplicateKeyError:
					print(f"A customer with _id={id_} already exists.")

			elif choice == 2:
				print("\nAll Customers:")
				for customer in collection.find():
					# Pretty-print the document
					print(customer)

			elif choice == 3:
				edit_id = input_int("Enter Customer ID to edit: ")
				new_name = input("Enter new Name: ").strip()
				new_city = input("Enter new City: ").strip()
				new_age = input_int("Enter new Age: ")
				new_active = input_bool("Is Active (true/false): ")

				update_result = collection.update_one(
					{"_id": edit_id},
					{"$set": {"name": new_name, "city": new_city, "age": new_age, "active": new_active}},
				)
				if update_result.matched_count:
					print("Customer updated successfully!")
				else:
					print(f"No customer found with _id={edit_id}.")

			elif choice == 4:
				del_id = input_int("Enter Customer ID to delete: ")
				delete_result = collection.delete_one({"_id": del_id})
				if delete_result.deleted_count:
					print("Customer deleted successfully!")
				else:
					print(f"No customer found with _id={del_id}.")

			elif choice == 5:
				print("Exiting...")
				break

			else:
				print("Invalid choice!")
	finally:
		client.close()


if __name__ == "__main__":
	main()

