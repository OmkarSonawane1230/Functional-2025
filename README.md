# Functional-2025

This setup i recommmend for only `github codespace`

using following commands to install mongodb shell in codespace easily but rather than mongo we use mongosh

```
bash

sudo apt update
sudo apt install -y gnupg curl
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-mongosh
```


if the mongosh show this kind of error run this command


```
error

$ mongosh
Current Mongosh Log ID: 690df8618aedaac00d9dc29c
Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.9
MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27017
```
Solution

```
bash

sudo apt-get install -y mongodb-org
sudo mkdir -p /data/db
sudo chown -R "$(whoami)" /data/db
mongod --dbpath /data/db --bind_ip 127.0.0.1 --fork --logpath /tmp/mongod.log
```

# Update the package index
sudo apt update

# Install the MySQL server
sudo apt install mysql-server

# To check if the MySQL service is running
sudo service mysql status

# To start the MySQL service (if not running)
sudo service mysql start

# To log in to the MySQL server as the root user
sudo mysql

# To exit the MySQL shell
exit