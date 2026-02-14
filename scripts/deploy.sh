#!/bin/bash

# Docer Deployment Script for EC2
set -e

echo "🚀 Starting Docer deployment..."

# 1. Update and install dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# 2. Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installed successfully."
else
    echo "✅ Docker is already installed."
fi

# 3. Install Docker Compose if not present
if ! docker compose version &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo apt-get install -y docker-compose-plugin
else
    echo "✅ Docker Compose is already installed."
fi

# 4. Deployment logic
if [ -d ".git" ]; then
    echo "📥 Pulling latest changes..."
    git pull origin main
else
    echo "⚠️ Not a git repository. Skipping git pull."
fi

# 5. Build and run
echo "🏗️ Building and starting containers..."
docker compose up --build -d

echo "✨ Deployment complete! Docer is running on port 8000."
echo "Check logs with: docker compose logs -f"
