# Hive on cluster
1. Deploy postgres
```
helm install postgresql ./hive/postgresql-16.5.0/postgresql \
  --namespace hive \
  --set auth.username=hive \
  --set auth.password=hive \
  --set auth.database=hive \
  --set primary.extendedConfiguration="password_encryption=md5" \
  --wait
```
2. Deploy Stackable operators
```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm repo update
helm install --wait commons-operator stackable-stable/commons-operator --version 25.3.0 
helm install --wait secret-operator stackable-stable/secret-operator --version 25.3.0 
helm install --wait listener-operator stackable-stable/listener-operator --version 25.3.0 
helm install --wait hive-operator stackable-stable/hive-operator --version 25.3.0 -n hive
```
3. Deploy hive cluster
```
kubectl apply -f ./hive/cluster/hive-s3-credentials.yaml -n hive --wait # Need to create as following
kubectl apply -f ./hive/cluster/hive-s3-secret-class.yaml -n hive --wait
kubectl apply -f ./hive/cluster/s3-connection.yaml -n hive --wait
kubectl apply -f ./hive/cluster/hive-postgres-s3.yaml -n hive --wait
```
```
hive-s3-credentials.yaml

---
apiVersion: v1
kind: Secret
metadata:
  name: hive-s3-secret
  labels:
    secrets.stackable.tech/class: hive-s3-secret-class
stringData:
  accessKey: 
  secretKey: 
```
4. Check hive works:
```
kubectl get statefulset -n hive
```
5. Edit resources of hive:
```
KUBE_EDITOR="nano" kubectl edit statefulset hive-postgres-s3-metastore-default -n hive
```
**Minimum HA requirements:
A minimal HA setup consisting of 2 Hive metastore instances has the following resource requirements:
- 100m CPU request
- 3000m CPU limit
- 1792Mi memory request and limit**