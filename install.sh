#!/bin/bash

# Update package manager
sudo apt update

# Install Node.js and npm
sudo apt install -y nodejs npm

# Install Docker and Docker Compose
sudo apt install -y docker.io docker-compose

# Clone the repository
git clone https://github.com/fin-officer/www

# Go to the repository directory
cd www

# Build and start the Docker containers
sudo docker-compose up --build -d

# Install dependencies
sudo docker exec -it www_app_1 npm install

# Start the Vue.js application
sudo docker exec -it www_app_1 npm run start

# Output success message
echo "Environment setup and application started successfully!"
