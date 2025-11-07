#!/usr/bin/env bash
set -e

echo "🔧 Installing MongoDB Shell (mongosh)..."

# Install dependencies
sudo apt-get update -y
sudo apt-get install -y gnupg curl

# Add MongoDB GPG key and repository (for Ubuntu Jammy)
if [ ! -f /usr/share/keyrings/mongodb-server-6.0.gpg ]; then
  curl -fsSL https://pgp.mongodb.com/server-6.0.asc \
    | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
fi

echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" \
  | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list > /dev/null

# Install MongoDB shell only
sudo apt-get update -y
sudo apt-get install -y mongodb-mongosh

echo "✅ mongosh installed successfully!"
mongosh --version

sudo apt-get install -y mongodb-org
sudo mkdir -p /data/db
sudo chown -R "$(whoami)" /data/db
mongod --dbpath /data/db --bind_ip 127.0.0.1 --fork --logpath /tmp/mongod.log

