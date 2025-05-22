# Nifi
1. Deploy operators
```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm repo update
helm install --wait commons-operator stackable-stable/commons-operator --version 25.3.0 -n nifi
helm install --wait secret-operator stackable-stable/secret-operator --version 25.3.0 -n nifi
helm install --wait listener-operator stackable-stable/listener-operator --version 25.3.0 -n nifi
helm install --wait zookeeper-operator stackable-stable/zookeeper-operator --version 25.3.0 -n nifi
helm install --wait nifi-operator stackable-stable/nifi-operator --version 25.3.0 -n nifi
```
2. Deploy cluster:
```
kubectl apply -n nifi -f ./nifi/cluster/zk.yaml --wait
kubectl apply -n nifi -f ./nifi/cluster/nifi-znode.yaml --wait
kubectl apply -n nifi -f ./nifi/cluster/nifi-credentials.yaml --wait # create as following
kubectl apply -n nifi -f ./nifi/cluster/nifi.yaml --wait
```
```
---
apiVersion: v1
kind: Secret
metadata:
  name: simple-admin-credentials
stringData:
  admin: admin
---
apiVersion: authentication.stackable.tech/v1alpha1
kind: AuthenticationClass
metadata:
  name: simple-nifi-users
spec:
  provider:
    static:
      userCredentialsSecret:
        name: simple-admin-credentials
```