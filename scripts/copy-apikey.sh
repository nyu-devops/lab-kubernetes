#!/bin/bash
echo "Copying IBM Cloud apikey into development environment..."
docker cp ~/.bluemix/apikey.json lab-kubernetes:/home/vscode 
docker exec lab-kubernetes sudo chown vscode:vscode /home/vscode/apikey.json
echo "Complete"
