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