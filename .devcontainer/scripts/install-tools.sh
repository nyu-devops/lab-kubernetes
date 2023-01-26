#!/bin/bash
######################################################################
# These scripts are meant to be run in user mode as they modify
# usr settings line .bashrc and .bash_aliases
######################################################################

echo "**********************************************************************"
echo "Installing K3D Kubernetes..."
echo "**********************************************************************"
curl -s "https://raw.githubusercontent.com/rancher/k3d/main/install.sh" | sudo bash
echo "Creating kc and kns alias for kubectl..."
echo "alias kc='/usr/local/bin/kubectl'" >> $HOME/.bash_aliases
echo "alias kns='kubectl config set-context --current --namespace'" >> $HOME/.bash_aliases

echo "**********************************************************************"
echo "Install Kustomize CLI..."
echo "**********************************************************************"
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/kustomize
echo "Creating ku alias for kustomize..."
echo "alias ku='/usr/local/bin/kustomize'" >> $HOME/.bash_aliases

echo "**********************************************************************"
echo "Install Tekton CLI..."
echo "**********************************************************************"
if [ $(uname -m) == aarch64 ]; then
    echo "Installing Tekton for ARM64..."
    curl https://github.com/tektoncd/cli/releases/download/v0.26.1/tkn_0.26.1_Linux_arm64.tar.gz --output tekton.tar.gz
else
    echo "Installing Tekton for x86_64..."
    curl https://github.com/tektoncd/cli/releases/download/v0.26.1/tkn_0.26.1_Linux_x86_64.tar.gz --output tekton.tar.gz
fi;
sudo tar xvzf tekton.tar.gz -C /usr/local/bin/ tkn
sudo ln -s /usr/local/bin/tkn /usr/bin/tkn
rm tekton.tar.gz

echo "**********************************************************************"
echo "Install Knative CLI..."
echo "**********************************************************************"
if [ $(uname -m) == aarch64 ]; then
    echo "Installing Knative for ARM64..."
    wget -q https://github.com/knative/client/releases/download/knative-v1.9.0/kn-linux-arm64 -O kn
else
    echo "Installing Knative for x86_64..."
    wget -q https://github.com/knative/client/releases/download/knative-v1.9.0/kn-linux-amd64 -O kn
fi;
chmod +x kn
sudo install kn /usr/local/bin
rm kn

echo "**********************************************************************"
echo "Installing IBM Cloud CLI..."
echo "**********************************************************************"
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
echo "source /usr/local/ibmcloud/autocomplete/bash_autocomplete" >> $HOME/.bashrc
# Install user mode IBM Cloud plugins
ibmcloud plugin install container-registry -r 'IBM Cloud'
ibmcloud plugin install kubernetes-service -r 'IBM Cloud'
ibmcloud plugin install cloud-object-storage -r 'IBM Cloud'
echo "Creating aliases for ibmcloud tools..."
echo "alias ic='/usr/local/bin/ibmcloud'" >> $HOME/.bash_aliases

# echo "**********************************************************************"
# echo "Install OpenShift CLI..."
# echo "**********************************************************************"
# curl https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz --output oc.tar.gz
# sudo tar xvzf oc.tar.gz -C /usr/local/bin/ oc
# sudo ln -s /usr/local/bin/oc /usr/bin/oc
# rm oc.tar.gz

# Platform specific installs
if [ $(uname -m) == aarch64 ]; then
    echo "Installing YQ for ARM64..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64
else
    echo "Installing YQ for x86_64..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
fi;
sudo chmod a+x /usr/local/bin/yq
