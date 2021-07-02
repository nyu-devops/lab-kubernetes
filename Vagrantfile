# -*- mode: ruby -*-
# vi: set ft=ruby :

######################################################################
# Kubernetes Minikube Environment
######################################################################
Vagrant.configure(2) do |config|
  # config.vm.box = "bento/ubuntu-20.04"
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "kubernetes"
  # config.vm.hostname = "ubuntu" 

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Mac users can comment this next line out but
  # Windows users need to change the permission of files and directories
  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=755,fmode=644"]

  ############################################################
  # Configure Vagrant to use VirtualBox on Intel:
  ############################################################
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "4096"
    vb.cpus = 2
    # Fixes some DNS issues on some networks
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  ############################################################
  # Configure Vagrant to use for Docker on Intel or ARM
  ############################################################
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:ubuntu"
    docker.remains_running = true
    docker.has_ssh = true
    docker.privileged = true
    docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:ro"]
    # Uncomment to force arm64 for testing images on Intel
    # docker.create_args = ["--platform=linux/arm64"]
  end

  ############################################################
  # Copy some host files to configure VM like the host
  ############################################################

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end

  # Copy your .vimrc file so that your VI editor looks right
  if File.exists?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  # Copy your IBM Clouid API Key if you have one
  if File.exists?(File.expand_path("~/.bluemix/apiKey.json"))
    config.vm.provision "file", source: "~/.bluemix/apiKey.json", destination: "~/.bluemix/apiKey.json"
  end

  ######################################################################
  # Create a Python 3 development environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Install Python 3 and dev tools 
    apt-get update
    apt-get install -y git vim tree wget jq build-essential python3-dev python3-pip python3-venv apt-transport-https
    apt-get upgrade python3
    
    # Create a Python3 Virtual Environment and Activate it in .profile
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    
    # Install app dependencies in virtual environment as vagrant user
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && pip install -U pip && pip install wheel'
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && pip install docker-compose'
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'

    # Check versions to prove that everything is installed
    python3 --version
  SHELL

  ############################################################
  # Provision Docker with Vagrant before starting kubernetes
  ############################################################
  config.vm.provision "docker" do |d|
    d.pull_images "alpine"
    d.pull_images "python:3.8-slim"
    d.pull_images "redis:6-alpine"
    d.run "redis:6-alpine",
      args: "--restart=always -d --name redis -p 6379:6379 -v redis:/data"
  end

  # ############################################################
  # # Install Kuberrnetes CLI
  # ############################################################
  # config.vm.provision "shell", inline: <<-SHELL
  #   # Install kubectl
  #   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/$(dpkg --print-architecture)/kubectl"
  #   install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  #   rm kubectl
  #   echo "alias kc='/usr/local/bin/kubectl'" >> /home/vagrant/.bash_aliases
  #   chown vagrant:vagrant /home/vagrant/.bash_aliases
  # SHELL
  
  # ############################################################
  # # Create a Kubernetes Cluster wiith K3D
  # ############################################################
  # config.vm.provision "shell", inline: <<-SHELL
  #   # Install K3d
  #   curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
  #   sudo -H -u vagrant sh -c "k3d registry create registry.localhost --port 50000"
  #   sudo -H -u vagrant sh -c "k3d cluster create mycluster --registry-use k3d-registry.localhost:50000 --agents 1 --port '8080:80@loadbalancer'"
  # SHELL

  ############################################################
  # Create a Kubernetes Cluster with MicroK8s
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # install MicroK8s version of Kubernetes
    sudo snap install microk8s --classic
    sudo microk8s.enable dns
    sudo microk8s.enable dashboard
    sudo microk8s.enable ingress
    sudo microk8s.enable registry
    sudo usermod -a -G microk8s vagrant
    sudo -H -u vagrant sh -c 'echo "alias kubectl=/snap/bin/microk8s.kubectl" >> ~/.bashrc'
    /snap/bin/microk8s.kubectl version --short
    
    # # Create aliases for microk8s=mk and kubecl=kc
    # echo "alias mk='/snap/bin/microk8s'" >> /home/vagrant/.bash_aliases
    # #echo "alias kc='/snap/bin/kubectl'" >> /home/vagrant/.bash_aliases
    # chown vagrant:vagrant /home/vagrant/.bash_aliases
    # # Set up Kubernetes context
    # sudo -H -u vagrant sh -c 'mkdir ~/.kube && microk8s.kubectl config view --raw > ~/.kube/config'
    # kubectl version --short  
    # microk8s.config > /home/vagrant/.kube/config
    # chown vagrant:vagrant /home/vagrant/.kube/config
    # chmod 600 /home/vagrant/.kube/config
    
  SHELL

  # ######################################################################
  # # Setup an IBM Cloud and Kubernetes environment
  # ######################################################################
  # config.vm.provision "shell", inline: <<-SHELL
  #   echo "\n************************************"
  #   echo " Installing IBM Cloud CLI..."
  #   echo "************************************\n"
  #   # Install IBM Cloud CLI as Vagrant user
  #   sudo -H -u vagrant sh -c 'curl -sL https://ibm.biz/idt-installer | bash'
  #   sudo -H -u vagrant sh -c 'ibmcloud config --usage-stats-collect false'
  #   sudo -H -u vagrant sh -c "echo 'source <(kubectl completion bash)' >> ~/.bashrc"
  #   sudo -H -u vagrant sh -c "echo alias ic=/usr/local/bin/ibmcloud >> ~/.bash_aliases"
  #   # Install OpenShift Client (optional)
  #   # mkdir ./openshift-client
  #   # cd openshift-client
  #   # wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz
  #   # tar xzf openshift-client-linux.tar.gz
  #   # cp kubectl /usr/local/bin
  #   # cp oc /usr/local/bin
  #   # cd ..
  #   # rmdir -fr ./openshift-client
  #   #
  #   # Install the IBM Cloud Native Toolkit
  #   # curl -sL shell.cloudnativetoolkit.dev | sh - && . ~/.bashrc
  #   echo "\n"
  #   echo "\n************************************"
  #   echo " For the Kubernetes Dashboard use:"
  #   echo " kubectl proxy --address='0.0.0.0'"
  #   echo "************************************\n"
  #   # Prove that plug-ins are installed as vagrant user
  #   sudo -H -u vagrant bash -c "bx plugin list"
  # SHELL

end
