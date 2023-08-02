# Docker and Kubernetes Lab

[![Build Status](https://github.com/nyu-devops/lab-kubernetes/actions/workflows/workflow.yaml/badge.svg)](https://github.com/nyu-devops/lab-kubernetes/actions)

What is Docker? How can Docker containers help you build and deploy a cloud native solution as micro-services? This lab will teach you what-you-need-to-know to get started building and running Docker Containers in IBM Cloud. It covers what Docker is, and more importantly, what Docker is not! You will learn how to deploy and run existing Docker community images, how to create your own Docker images and push them to IBM Cloud, and how to connect containers together using Docker Compose. If you want to know what all this fuss about containers is about, come to this lab and spin up a few containers and see for yourself why everyone is adopting Docker.

This lab is an example of how to create a Python / Flask / Redis app using Docker on IBM Cloud

### Copy your apikey to /home/vscode

```
docker cp ~/.bluemix/apikey.json lab-kubernetes:/home/vscode
docker exec lab-kubernetes sudo chown vscode:vscode /home/vscode/apikey.json
```

### IBM Cloud Login

```
ibmcloud login -a cloud.ibm.com -r us-south -g default --apikey @~/apikey.json
ibmcloud ks cluster config --cluster nyu-devops
ibmcloud cr login
```

### Update Image name

```
(kustomize edit set image hitcounter=us.icr.io/nyu_devops/lab-kubernetes && kustomize build .)
```

```
kustomize build kube/overlays/dev | kc apply -f -  
```

### Create a dev namespace

When you create a new namespace you must copy the `ImagePullSecret` from the `default` namespace so that deployments in the new namespace can pull images from the IBM Cloud Container Registry.

The command to do this for `dev` is:

```bash
kunectl create namespace dev
kubectl -n default get secret all-icr-io -o yaml | sed 's/default/dev/g' | kubectl -n dev apply -f -
```

What the second command does is to get the `ImagePullSecret` named `all-icr-io` from the `default` namespace and running it through `sed` to change the `namespace:` to whatever is needed, and applying it to the `dev` namespace.

### Use with Minikube

In order to use Minikube you need to enable the ingress and registry addons.

Here are the commands to get `minikube` working:

```bash
minikube start
minikube addons enable ingress
minikube addons enable registry
```

You can also specify these are start up with:

```bash
minikube start --addons ingress --addons registry
```

See Minikube [documentation](https://minikube.sigs.k8s.io/docs/start/) for reference.
