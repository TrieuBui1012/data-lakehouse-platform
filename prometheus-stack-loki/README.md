# Prometheus Stack - Install from Rancher UI
Step-by-step:
1. Click ☰ > Cluster Management.
2. Go to the cluster that you created and click Explore.
3. Click Cluster Tools (bottom left corner).
4. Click Install by Monitoring.
5. Optional: Customize requests, limits and more for Alerting, Prometheus, and Grafana in the Values step. For help, refer to the configuration reference. For example, to enable angular support dashboard for grafana, configure yaml file:
```
grafana.grafana.ini.security.angular_support_enabled: true
```
# Loki
1. Add Grafana’s chart repository to Helm:
```helm repo add grafana https://grafana.github.io/helm-charts```
2. Update the chart repository:
```helm repo update```
3. Deploy Loki using the configuration file values.yaml:
- To install:
```helm install --values prometheus-stack-loki/values.yaml loki grafana/loki -n cattle-monitoring-system```
- To upgrade:
```helm upgrade --values prometheus-stack-loki/values.yaml loki grafana/loki -n cattle-monitoring-system```
4. Verify that Loki is running:
```kubectl get pods -n cattle-monitoring-system```
The values.yaml file for Loki (official): https://github.com/grafana/loki/blob/main/production/helm/loki/values.yaml
Define your own values file for Loki.

**Note: Need to increase Grafana resource**

# Fluent Bit & Fluentd
Expose logs to http://loki-gateway