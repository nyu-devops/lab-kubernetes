#!/bin/bash

echo "Installing IBM Cloud CLI" 
wget https://download.clis.cloud.ibm.com/ibm-cloud-cli/2.6.0/IBM_Cloud_CLI_2.6.0_arm64.tar.gz
tar xzvf IBM_Cloud_CLI_2.6.0_arm64.tar.gz
install Bluemix_CLI/bin/ibmcloud /usr/local/bin/ibmcloud
rm -fr Bluemix_CLI/
