#!/bin/bash

echo "🗄️ MySQL Multi-Language Setup Wizard"
echo "===================================="

# Flags
INSTALL_MYSQL=false
INSTALL_NODE=false
INSTALL_PYTHON=false
INSTALL_JAVA=false
INSTALL_CPP=false

# Ask user choices
read -p "Do you want to set up MySQL Server? (y/n): " ans
[[ "$ans" == "y" ]] && INSTALL_MYSQL=true

read -p "Do you want to set up Node.js Integration? (y/n): " ans
[[ "$ans" == "y" ]] && INSTALL_NODE=true

read -p "Do you want to set up Python Integration? (y/n): " ans
[[ "$ans" == "y" ]] && INSTALL_PYTHON=true

read -p "Do you want to set up Java Integration? (y/n): " ans
[[ "$ans" == "y" ]] && INSTALL_JAVA=true

read -p "Do you want to set up C++ Integration? (y/n): " ans
[[ "$ans" == "y" ]] && INSTALL_CPP=true

echo ""
echo "⚙️ Starting installation based on your choices..."
echo "------------------------------------"

# MySQL
if $INSTALL_MYSQL; then
    echo "🔧 Installing and starting MySQL..."
    sudo apt update
    sudo apt install -y mysql-server
    sudo service mysql start

    echo "🔒 Fixing MySQL socket permissions..."
    sudo chown -R mysql:mysql /var/run/mysqld
    sudo chmod 755 /var/run/mysqld
    sudo service mysql restart

    echo "⚙️ Setting up MySQL root user and database..."
    sudo mysql -u root <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mysql123';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS Testing;
USE Testing;
CREATE TABLE IF NOT EXISTS Temp (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  login_status VARCHAR(255) DEFAULT 'Setup Script'
);
EOF
    echo "✅ MySQL setup complete."
fi

# Node.js
if $INSTALL_NODE; then
    echo "🟢 Setting up Node.js..."
    mkdir -p nodejs_project && cd nodejs_project
    npm init -y
    npm install mysql2
    cd ..
    echo "✅ Node.js setup complete (project in ./nodejs_project)."
fi

# Python
if $INSTALL_PYTHON; then
    echo "🐍 Setting up Python..."
    sudo apt install -y python3 python3-pip
    pip3 install mysql-connector-python
    echo "✅ Python setup complete."
fi

# Java
if $INSTALL_JAVA; then
    echo "☕ Setting up Java Integration..."
    mkdir -p lib
    cd lib
    wget -nc https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/9.3.0/mysql-connector-j-9.3.0.jar
    cd ..
    echo "✅ Java setup complete (Connector in ./java_project/lib/)."
    echo "👉 To compile: javac -cp .:java_project/lib/mysql-connector-j-9.3.0.jar MySQLInJava.java"
    echo "👉 To run: java -cp .:java_project/lib/mysql-connector-j-9.3.0.jar MySQLInJava"
fi

# C++
if $INSTALL_CPP; then
    echo "🧾 Setting up C++..."
    sudo apt install -y g++ libmysqlcppconn-dev
    echo "✅ C++ setup complete."
fi

echo ""
echo "🎉 Setup finished!"
if $INSTALL_MYSQL; then
    echo "------------------------------------"
    echo "📌 MySQL Login Details:"
    echo "   Username: root"
    echo "   Password: mysql123"
    echo "   Database: Testing"
    echo "------------------------------------"
    echo "👉 To log in, run: mysql -u root -p"
    echo "   (then enter mysql123 when asked)"
fi
