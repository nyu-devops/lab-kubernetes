#!/bin/bash
echo "Creating Kubernetes cluster with a registry..."
k3d cluster create --registry-create cluster-registry:0.0.0.0:32000 --port '8080:80@loadbalancer'
echo "Complete."