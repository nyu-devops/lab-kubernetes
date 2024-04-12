#!/bin/bash
echo "Setting up Kubernetes lab environment..."
docker pull python:3.11-slim
docker run -d --name redis --restart always -p 6379:6379 -v redis:/data redis:6-alpine

echo Setting up registry.local...
sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"

echo "Make git stop complaining about unsafe folders..."
git config --global --add safe.directory /app

echo "Setup complete"
