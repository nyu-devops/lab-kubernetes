# -*- mode: ruby -*-
# vi: set ft=ruby :

######################################################################
# Kubernetes Minikube Environment
######################################################################
Vagrant.configure(2) do |config|
  # config.vm.box = "ubuntu/focal64"
  # config.vm.hostname = "ubuntu" 
  # config.vm.box = "debian/buster64"
  # config.vm.box = "debian/bullseye64"
  config.vm.box = "bento/ubuntu-21.04"
  config.vm.hostname = "kubernetes"

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8090, host: 8090, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.56.10"

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
    #vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    #vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  ############################################################
  # Configure Vagrant to use for Docker on Intel or ARM
  ############################################################
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:debian"
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

  # Copy your IBM Cloud API Key if you have one
  if File.exists?(File.expand_path("~/.bluemix/apikey.json"))
    config.vm.provision "file", source: "~/.bluemix/apikey.json", destination: "~/.bluemix/apikey.json"
  end

  ######################################################################
  # Create a Python 3 development environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Install Python 3 and dev tools 
    apt-get update
    apt-get install -y git vim tree wget jq python3-dev python3-pip python3-venv apt-transport-https
    apt-get upgrade python3
    
    # Create a Python3 Virtual Environment and Activate it in .profile
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    
    # Install app dependencies in virtual environment as vagrant user
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && 
      cd /vagrant &&
      pip install -U pip wheel && 
      pip install docker-compose &&
      pip install -r requirements.txt'

      # Check versions to prove that everything is installed
      python3 --version

      # Create .env file if it doesn't exist
      sudo -H -u vagrant sh -c 'cd /vagrant && if [ ! -f .env ]; then cp dot-env-example .env; fi'    
  SHELL

  ############################################################
  # Provision Docker with Vagrant before starting kubernetes
  ############################################################
  config.vm.provision "docker" do |d|
    d.pull_images "alpine"
    d.pull_images "python:3.9-slim"
    d.pull_images "redis:6-alpine"
    d.run "redis:6-alpine",
      args: "--restart=always -d --name redis -p 6379:6379 -v redis:/data"
  end

  ############################################################
  # Install Kubernetes CLI and Helm
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Install kubectl
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/$(dpkg --print-architecture)/kubectl"
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
    echo "alias kc='/usr/local/bin/kubectl'" >> /home/vagrant/.bash_aliases
    chown vagrant:vagrant /home/vagrant/.bash_aliases
    # Install helm
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
  SHELL
  
  ############################################################
  # Create a Kubernetes Cluster wiith K3D
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Install K3d
    curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
    # echo "127.0.0.1 k3d-registry.localhost" >> /etc/hosts
    # sudo -H -u vagrant sh -c "k3d registry create registry.localhost --port 50000"
    # sudo -H -u vagrant sh -c "k3d cluster create devops --registry-use k3d-registry.localhost:50000 --agents 1 --port '8080:80@loadbalancer'"
  SHELL

  ######################################################################
  # Setup a IBM Cloud and Kubernetes environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    echo "\n************************************"
    echo " Installing IBM Cloud CLI..."
    echo "************************************\n"
    # Install IBM Cloud CLI as Vagrant user
    sudo -H -u vagrant sh -c '
    curl -fsSL https://clis.cloud.ibm.com/install/linux | sh && \
    ibmcloud plugin install container-service && \
    ibmcloud plugin install container-registry && \
    echo "alias ic=ibmcloud" >> ~/.bashrc
    '

    # Show completion instructions
    sudo -H -u vagrant sh -c "echo alias ic=/usr/local/bin/ibmcloud >> ~/.bash_aliases"
    echo "\n************************************"
    echo "If you have an IBM Cloud API key in ~/.bluemix/apiKey.json"
    echo "You can login with the following command:"
    echo "\n"
    echo "ibmcloud login -a https://cloud.ibm.com --apikey @~/.bluemix/apikey.json -r us-south"
    echo "ibmcloud ks cluster config --cluster <your-cluster-name>"
    echo "\n************************************"
  SHELL

end
