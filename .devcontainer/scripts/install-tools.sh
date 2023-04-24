#!/bin/bash
######################################################################
# These scripts are meant to be run in user mode as they modify
# usr settings line .bashrc and .bash_aliases
######################################################################

echo "**********************************************************************"
echo "Establishing Architecture..."
echo "**********************************************************************"
ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
echo "Architecture is:" $ARCH

echo "**********************************************************************"
echo "Installing DevSpace..."
echo "**********************************************************************"
curl -L -o devspace "https://github.com/loft-sh/devspace/releases/latest/download/devspace-linux-$ARCH"
sudo install -c -m 0755 devspace /usr/local/bin

echo "**********************************************************************"
echo "Installing K9s..."
echo "**********************************************************************"
curl -L -o k9s.tar.gz "https://github.com/derailed/k9s/releases/download/v0.27.3/k9s_Linux_$ARCH.tar.gz"
tar xvzf k9s.tar.gz
sudo install -c -m 0755 k9s /usr/local/bin
rm k9s.tar.gz

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
echo "Installing IBM Cloud CLI..."
echo "**********************************************************************"
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
echo "source /usr/local/ibmcloud/autocomplete/bash_autocomplete" >> $HOME/.bashrc
# Install user mode IBM Cloud plugins
ibmcloud plugin install container-registry -r 'IBM Cloud'
ibmcloud plugin install kubernetes-service -r 'IBM Cloud'
echo "Creating aliases for ibmcloud tools..."
echo "alias ic='/usr/local/bin/ibmcloud'" >> $HOME/.bash_aliases

echo "**********************************************************************"
echo "Installing YQ..."
echo "**********************************************************************"
sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_$ARCH
sudo chmod a+x /usr/local/bin/yq
