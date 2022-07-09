#!/bin/bash

echo "Installing IBM Cloud CLI..."
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh

echo "Creating alias 'ic' for ibmcloud command"
echo "alias ic='/usr/local/bin/ibmcloud'" >> ~/.bash_aliases

echo "Installing Kubernetes Service Plugin..."
ibmcloud plugin install container-service -r 'IBM Cloud'

echo "Installing Container Registry Plugin..."
ibmcloud plugin install container-registry -r 'IBM Cloud'

echo "--- IBM Cloud CLI installation complete ---"

# Platform specific installs
if [ $(uname -m) == aarch64 ]; then
    echo "Installing YQ for ARM64..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64
    sudo chmod a+x /usr/local/bin/yq
else
    echo "Installing YQ for x86_64..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    sudo chmod a+x /usr/local/bin/yq
fi;
