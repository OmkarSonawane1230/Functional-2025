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