#!/bin/bash

# Add the IBM Cloud CLI if not ARM architecture
if [ $(uname -m) == aarch64 ]; then
    echo "Installing IBM Cloud CLI for ARM64" 
    wget https://download.clis.cloud.ibm.com/ibm-cloud-cli/2.6.0/IBM_Cloud_CLI_2.6.0_arm64.tar.gz
    tar xzvf IBM_Cloud_CLI_2.6.0_arm64.tar.gz
    install Bluemix_CLI/bin/ibmcloud /usr/local/bin/ibmcloud
    rm -fr Bluemix_CLI/
else
    echo "Installing IBM Cloud CLI..."
    curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
    echo "alias ic=ibmcloud" >> /home/devops/.bashrc
    echo "Installing Cloud Foundry CLI..."
    ibmcloud cf install -f
fi;


