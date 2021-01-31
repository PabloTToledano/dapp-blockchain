#!/usr/bin/env bash
#only works with minikube =<1.15.1
echo "Do you want to start minikube? Y/n"
read -p "Y/n: " input
if [ "$input" = "Y" ]; then
    echo "Starting minikube"
    minikube start --cpus 4 --memory 4096 --kubernetes-version v1.14.2 --driver=docker
    minikube kubectl -- get pods -A
    #eval $(minikube docker-env)
fi
./blockchainit
kubectl apply -f yaml/
