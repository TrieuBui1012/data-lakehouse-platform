# Spark
1. Deploy operators
```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm repo update
helm install --wait commons-operator stackable-stable/commons-operator --version 25.3.0 
helm install --wait secret-operator stackable-stable/secret-operator --version 25.3.0 
helm install --wait listener-operator stackable-stable/listener-operator --version 25.3.0 
helm install --wait spark-k8s-operator stackable-stable/spark-k8s-operator --version 25.3.0 -n spark
```
2. Deploy Spark History Server
```
kubectl apply -f ./spark/cluster/history-secret-class.yaml -n spark --wait
kubectl apply -f ./spark/cluster/history-s3-credentials.yaml -n spark --wait
kubectl apply -f ./spark/cluster/s3-secret-class.yaml -n spark --wait
kubectl apply -f ./spark/cluster/s3-credentials.yaml -n spark --wait
kubectl apply -f ./spark/cluster/spark-history-server.yaml -n spark --wait
```