# Kafka stackable
1. Deploy operators
```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm repo update
helm install --wait commons-operator stackable-stable/commons-operator --version 25.3.0 
helm install --wait secret-operator stackable-stable/secret-operator --version 25.3.0 
helm install --wait listener-operator stackable-stable/listener-operator --version 25.3.0 
helm install --wait zookeeper-operator stackable-stable/zookeeper-operator --version 25.3.0 -n kafka
helm install --wait kafka-operator stackable-stable/kafka-operator --version 25.3.0 -n kafka
```
2. Deploy zookeeper cluster
```
kubectl apply -f ./kafka/cluster/zookeeper.yaml -n kafka --wait
kubectl apply -f ./kafka/cluster/kafka-znode.yaml -n kafka --wait
kubectl apply --server-side -f ./kafka/cluster/kafka.yaml -n kafka --wait
```
3. Deploy UI
```
docker run -it -p 8080:8080 -e DYNAMIC_CONFIG_ENABLED=true ghcr.io/kafbat/kafka-ui
```