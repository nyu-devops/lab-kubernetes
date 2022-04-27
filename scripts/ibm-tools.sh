#!/bin/bash

# Add the IBM Cloud CLI for ARM and AMD architecture
if [ $(uname -m) == aarch64 ]; then
    echo "Installing IBM Cloud CLI for ARM64..." 
    wget https://download.clis.cloud.ibm.com/ibm-cloud-cli/2.6.0/binaries/IBM_Cloud_CLI_2.6.0_linux_arm64.tgz  
    tar xzvf IBM_Cloud_CLI_2.6.0_linux_arm64.tgz 
    sudo install IBM_Cloud_CLI/ibmcloud /usr/local/bin/ibmcloud
    rm -fr IBM_Cloud_CLI
    rm IBM_Cloud_CLI_2.6.0_linux_arm64.tgz
else
    echo "Installing IBM Cloud CLI for x86_64..."
    curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
fi;

echo "Creating alias 'ic' for ibmcloud command"
echo "alias ic='/usr/local/bin/ibmcloud'" >> ~/.bash_aliases

echo "Installing Kubernetes Plugin..."
ibmcloud plugin install container-service
echo "IBM Cloud CLI installation complete."
