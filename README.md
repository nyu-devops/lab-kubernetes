# Docker and Kubernetes Lab

[![Build Status](https://github.com/nyu-devops/lab-kubernetes/actions/workflows/workflow.yaml/badge.svg)](https://github.com/nyu-devops/lab-kubernetes/actions)

What is Docker? How can Docker containers help you build and deploy a cloud native solution as micro-services? This lab will teach you what-you-need-to-know to get started building and running Docker Containers in IBM Cloud. It covers what Docker is, and more importantly, what Docker is not! You will learn how to deploy and run existing Docker community images, how to create your own Docker images and push them to IBM Cloud, and how to connect containers together using Docker Compose. If you want to know what all this fuss about containers is about, come to this lab and spin up a few containers and see for yourself why everyone is adopting Docker.

This lab is an example of how to create a Python / Flask / Redis app using Docker on IBM Cloud

## Setting up your Development Environment

There are three ways to use this lab:

1. You can use Docker Desktop and Visual Studio Code with the Remote Containers extensions to run this lab in a Docker contaner development environment (preferred)
2. You can use Vagrant and VirtualBox to create a development environment in a local virtual machine.
3. You can Docker and the IBM Cloud CLI and IBM Container plug-in locally on your computer.

### Docker and Visual Studio Code

This option is preferred and is the only option if you have an Apple M1 Silicon Mac that is based on the ARM archotecture as VirtualBox does not support ARM.

This option also assumes that you have completed previous labs and have the following files exist your computer:

| Filename | Description |
| -------- | ----------- |
| ~/.gitconfig | Git configuration file |
| ~/.ssh/ | SSH keys folder |
| ~/.bluemix/ | IBM Cloud folder |

If you don't have all three of these the containers will fail to come up because these folders are shared with the container so that you can work in your development cotainer with the same identity and credentials as you do on your computer.

### Vagrant and VirtualBox (Intel only!)

We use Vagrant, VirtualBox, and Docker for virtualizing our development environment. Vagrant is technology that allows you to quickly provision and configure Linux virtual machines on your computer. VirtualBox is a hypervisor like VMware Fusion that hosts virtual machines. Docker is technology that will run multiple containers within a single Linux host machine. Together they make a powerful development environment that mimics multiple servers in a production environment.

To get started, download VirtualBox and Vagrant if you don't have them already:

Download [VirtualBox](https://www.virtualbox.org) - Used to host virtual machines locally on your workstation

Download [Vagrant](https://www.vagrantup.com) - Used to auto-provision VMs containing your complete dev environment

Install VirtualBox and then Vagrant. If you want to test with `cURL` you will need to have it installed on your laptop if your system doesn't already have it.

VirtualBox will install Docker into the virtual machine so you don't have to.

### Install using Vagrant and VirtualBox

    git clone https://github.com/nyu-devops/lab-kubernetes.git
    cd lab-kubernetes
    vagrant up
    vagrant ssh

#### Note: vagrant up
This `Vagrantfile` requires the `vagrant-docker-compose` plug-in. It will check for it and install it if it is not present. This will cause you to have to invoke `vagrant up` a second time. This is normal behavior.

If you see this when you `vagrant up`
```
Installing the 'vagrant-docker-compose' plugin. This can take a few minutes...
Fetching: vagrant-docker-compose-1.3.0.gem (100%)
Installed the plugin 'vagrant-docker-compose (1.3.0)'!
Dependencies installed, please try the command again.
```

Just issue `vagrant up` again.

### Installing on Mac OS X or Windows
Get Docker Toolbox from the Docker web site and install it:
https://www.docker.com/docker-toolbox

### Installing on Ubuntu Trusty 14.04 (LTS)

    sudo apt-get update
    sudo apt-get install docker-engine

Installing on Other OS See Docker installation guide:
https://docs.docker.com/installation/
