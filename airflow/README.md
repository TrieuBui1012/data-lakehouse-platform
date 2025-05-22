# Airflow
1. Install postgres
```
helm install airflow-postgresql oci://registry-1.docker.io/bitnamicharts/postgresql \
  --version 16.5.0 \
  --set auth.database=airflow \
  --set auth.username=airflow \
  --set auth.password=airflow \
  -n airflow \
  --wait
```
2. Install redis - if using celery
```
helm install airflow-redis oci://registry-1.docker.io/bitnamicharts/redis \
  --version 20.11.3 \
  --set replica.replicaCount=1 \
  --set auth.password=redis \
  -n airflow \
  --wait
```
3. Install operators:
```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm repo update
helm install --wait commons-operator stackable-stable/commons-operator --version 25.3.0 
helm install --wait secret-operator stackable-stable/secret-operator --version 25.3.0 
helm install --wait listener-operator stackable-stable/listener-operator --version 25.3.0 
helm install --wait airflow-operator stackable-stable/airflow-operator --version 25.3.0 -n airflow
```
4. Run these commands:
```
kubectl apply -f ./airflow/cluster/airflow-credentials.yaml -n airflow
kubectl apply -f ./airflow/cluster/git-credentials.yaml -n airflow # Need to create as following
kubectl apply -f ./airflow/cluster/airflow.yaml -n airflow
kubectl apply -f ./airflow/cluster/airflow-spark-clusterrole.yaml -n airflow
```
```
git-credentials.yaml:

---
apiVersion: v1
kind: Secret
metadata:
  name: git-credentials
type: Opaque
stringData:
  user: 
  password:
```
5. Add S3 connection in Airflow Web UI
In the Airflow Web UI, click on Admin → Connections → Add a new record (the plus). Then enter your MinIO host and credentials as shown.
The name or connection ID is minio, the type is Amazon Web Services, the AWS Access Key ID and AWS Secret Access Key are filled with the S3 credentials. The Extra field contains the endpoint URL like:
{
  "endpoint_url": "http://minio.default.svc.cluster.local:9000"
}

