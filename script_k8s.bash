#!/bin/bash

docker build -t bank-database ./Database
docker save bank-database > bank-database.tar
microk8s ctr image import bank-database.tar
rm bank-database.tar
microk8s kubectl apply -f ./k8s/database-statefulset.yaml
microk8s kubectl apply -f ./k8s/database-service.yaml