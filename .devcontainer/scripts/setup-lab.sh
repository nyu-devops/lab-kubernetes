#!/bin/bash
echo "Setting up Docker lab environment..."
docker pull python:3.11-slim
docker run --restart=always -d --name redis -p 6379:6379 -v redis:/data redis:6-alpine
echo Setting up registry.local...
sudo bash -c "echo '127.0.0.1    registry.local' >> /etc/hosts"
echo "Setup complete"