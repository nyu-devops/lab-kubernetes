#!/bin/bash
echo "Deleting Kubernetes cluster..."
k3d cluster delete
echo "Complete."