# Superset
1. Deploy operators
```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm repo update
helm install --wait commons-operator stackable-stable/commons-operator --version 25.3.0  
helm install --wait secret-operator stackable-stable/secret-operator --version 25.3.0 
helm install --wait listener-operator stackable-stable/listener-operator --version 25.3.0 
helm install --wait superset-operator stackable-stable/superset-operator --version 25.3.0 -n superset
```
2. Deploy postgres
```
helm install superset oci://registry-1.docker.io/bitnamicharts/postgresql \
    --version 16.5.0 \
    --set auth.username=superset \
    --set auth.password=superset \
    --set auth.database=superset \
    --wait -n superset
```
3. Deploy superset
```
helm install superset oci://registry-1.docker.io/bitnamicharts/postgresql \
    --version 16.5.0 \
    --set auth.username=superset \
    --set auth.password=superset \
    --set auth.database=superset \
    --wait -n superset
```
4. Deploy superset
```
kubectl apply -f ./superset/cluster/superset-credentials.yaml -n superset # create as following
kubectl apply -f ./superset/cluster/superset.yaml -n superset
```
```
---
apiVersion: v1
kind: Secret
metadata:
  name: simple-superset-credentials
type: Opaque
stringData:
  adminUser.username: admin
  adminUser.firstname: Superset
  adminUser.lastname: Admin
  adminUser.email: admin@superset.com
  adminUser.password: admin
  connections.secretKey: thisISaSECRET_1234
  connections.sqlalchemyDatabaseUri: postgresql://superset:superset@superset-postgresql.superset.svc.cluster.local/superset
```