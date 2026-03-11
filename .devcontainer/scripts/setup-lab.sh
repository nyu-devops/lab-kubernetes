#!/bin/bash
echo "**********************************************************************"
echo "Setting up Kubernetes lab environment..."
echo "**********************************************************************\n"

docker pull quay.io/rofrano/python:3.12-slim
docker run -d --name redis --restart always -p 6379:6379 -v redis:/data redis:6-alpine

echo Setting up registry.local...
sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"

echo "Make git stop complaining about unsafe folders..."
git config --global --add safe.directory /app

echo "Configuring insecure registry"
sudo cp ./config/insecure-registry.json /etc/docker/daemon.json
echo "Restarting Docker..."
sudo pkill dockerd && sudo pkill containerd
# ( dockerd > /tmp/dockerd.log 2>&1 ) &
bash /usr/local/share/docker-init.sh

echo "\n**********************************************************************"
echo "Setup complete"
echo "**********************************************************************"
