#!/bin/bash
echo "Creating IBM Cloud apikey..."
ibmcloud login
mkdir ~/.bluemix
ibmcloud iam api-key-create DevOps -d "NYU DevOps Class" --file ~/.bluemix/apikey.json 
echo "Complete"
