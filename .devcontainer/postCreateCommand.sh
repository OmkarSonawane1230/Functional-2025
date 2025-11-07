#!/usr/bin/env bash
set -e

echo "🔧 Setting up MongoDB inside Codespace..."

# Install dependencies
sudo apt-get update -y
sudo apt-get install -y gnupg curl

# Add MongoDB official GPG key and repo
if [ ! -f /usr/share/keyrings/mongodb-server-6.0.gpg ]; then
  curl -fsSL https://pgp.mongodb.com/server-6.0.asc \
    | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
fi

echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" \
  | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB server + shell
sudo apt-get update -y
sudo apt-get install -y mongodb-org mongodb-mongosh

# Create data directory
sudo mkdir -p /data/db
sudo chown -R "$(whoami)" /data/db

# Start MongoDB in the background
mongod --dbpath /data/db --bind_ip 127.0.0.1 --fork --logpath /tmp/mongod.log

echo "✅ MongoDB started successfully!"
