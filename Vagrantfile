# -*- mode: ruby -*-
# vi: set ft=ruby :

# WARNING: You will need the following plugin:
# vagrant plugin install vagrant-docker-compose
if Vagrant.plugins_enabled?
  unless Vagrant.has_plugin?('vagrant-docker-compose')
    puts 'Plugin missing.'
    system('vagrant plugin install vagrant-docker-compose')
    puts 'Dependencies installed, please try the command again.'
    exit
  end
end

######################################################################
# Kubernetes Minikube Environment
######################################################################
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.hostname = "kubernetes"

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # expose port 8080 in the guest VM to 8080 on the host computer
  config.vm.network "forwarded_port", guest: 80,   host: 1080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8001, host: 8001, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  ############################################################
  # Configure Vagrant to use VirtualBox:
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
  if File.exists?(File.expand_path("~/.ssh/id_rsa.pub"))
    config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/id_rsa.pub"
  end

  # Copy your .vimrc file so that your VI editor looks right
  if File.exists?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  # Copy your IBM Clouid API Key if you have one
  if File.exists?(File.expand_path("~/.bluemix/apiKey.json"))
    config.vm.provision "file", source: "~/.bluemix/apiKey.json", destination: "~/.bluemix/apiKey.json"
  end

  ############################################################
  # Create a Python 3 environment for development work
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Update and install
    apt-get update
    apt-get install -y git tree wget build-essential python3-dev python3-pip python3-venv apt-transport-https
    apt-get upgrade python3

    # Create a Python3 Virtual Environment and Activate it in .profile
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'
  SHELL

  ############################################################
  # Provision Docker with Vagrant before starting kubernetes
  ############################################################
  config.vm.provision "docker" do |d|
    d.pull_images "alpine"
    d.pull_images "python:3.7-slim"
    d.pull_images "redis:alpine"
    d.run "redis:alpine",
      args: "--restart=always -d --name redis -p 6379:6379 -v redis_volume:/data"
  end

  ############################################################
  # Add Docker compose
  ############################################################
  config.vm.provision :docker_compose
  # config.vm.provision :docker_compose,
  #   yml: "/vagrant/docker-compose.yml",
  #   rebuild: true,
  #   run: "always"

  ############################################################
  # Create a Kubernetes Cluster
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # install MicroK8s version of Kubernetes
    sudo snap install microk8s --classic
    sudo microk8s.enable dns dashboard registry
    sudo usermod -a -G microk8s vagrant
    sudo -H -u vagrant sh -c 'echo "alias kubectl=/snap/bin/microk8s.kubectl" >> ~/.bashrc'
    /snap/bin/microk8s.kubectl version --short
  SHELL


  ######################################################################
  # Setup an IBM Cloud and Kubernetes environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    echo "\n************************************"
    echo " Installing IBM Cloud CLI..."
    echo "************************************\n"
    # Install IBM Cloud CLI as Vagrant user
    sudo -H -u vagrant sh -c 'curl -sL http://ibm.biz/idt-installer | bash'
    sudo -H -u vagrant sh -c 'ibmcloud config --usage-stats-collect false'
    sudo -H -u vagrant sh -c "echo 'source <(kubectl completion bash)' >> ~/.bashrc"
    sudo -H -u vagrant sh -c "echo alias ic=/usr/local/bin/ibmcloud >> ~/.bash_aliases"
    echo "\n"
    echo "\n************************************"
    echo " For the Kubernetes Dashboard use:"
    echo " kubectl proxy --address='0.0.0.0'"
    echo "************************************\n"
    # Prove that plug-ins are installed as vagrant user
    sudo -H -u vagrant bash -c "bx plugin list"
  SHELL

  ############################################################
  # Start minikube as vagrant user but with sudo privileges
  ############################################################
  # sudo minikube start --vm-driver=none --memory 4096
  # sudo minikube addons enable ingress

end
