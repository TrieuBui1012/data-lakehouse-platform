# Rancher on a RKE2 cluster - 2 cpu, 6GB memory
First, you must create the directory where the RKE2 config file is going to be placed:
```
mkdir -p /etc/rancher/rke2/
```
Next, create the RKE2 config file at /etc/rancher/rke2/config.yaml using the following example:
```
token: my-shared-secret
tls-san:
  - your-ip-separated-by-hyphen.nip.io
  - or your dns
```
After that, you need to run the install command and enable and start rke2:
```
curl -sfL https://get.rke2.io | sh -
systemctl enable rke2-server.service
systemctl start rke2-server.service
```
To join the rest of the nodes, you need to configure each additional node with the same shared token or the one generated automatically. Here is an example of the configuration file:
```
    token: my-shared-secret
    server: https://<DNS-DOMAIN>:9345
    tls-san:
      - my-kubernetes-domain.com
      - another-kubernetes-domain.com
```
After that, you need to run the installer and enable, then start, rke2:
```
    curl -sfL https://get.rke2.io | sh -
    systemctl enable rke2-server.service
    systemctl start rke2-server.service
```
Once you've launched the rke2 server process on all server nodes, ensure that the cluster has come up properly with
```
/var/lib/rancher/rke2/bin/kubectl \
        --kubeconfig /etc/rancher/rke2/rke2.yaml get nodes
```
Then test the health of the cluster pods:
```
/var/lib/rancher/rke2/bin/kubectl \
        --kubeconfig /etc/rancher/rke2/rke2.yaml get pods --all-namespaces
```
When you installed RKE2 on each Rancher server node, a kubeconfig file was created on the node at /etc/rancher/rke2/rke2.yaml. This file contains credentials for full access to the cluster, and you should save this file in a secure location.
To use this kubeconfig file,
1. Install kubectl, a Kubernetes command-line tool.
2. Copy the file at /etc/rancher/rke2/rke2.yaml and save it to the directory ~/.kube/config on your local machine.
3. In the kubeconfig file, the server directive is defined as localhost. Configure the server as the DNS of your control-plane load balancer, on port 6443. (The RKE2 Kubernetes API Server uses port 6443, while the Rancher server will be served via the NGINX Ingress on ports 80 and 443.)
Result: You can now use kubectl to manage your RKE2 cluster. If you have more than one kubeconfig file, you can specify which one you want to use by passing in the path to the file when using kubectl:
```
kubectl --kubeconfig ~/.kube/config/rke2.yaml get pods --all-namespaces
```
Now that you have set up the kubeconfig file, you can use kubectl to access the cluster from your local machine.
Check that all the required pods and containers are healthy are ready to continue:
```
/var/lib/rancher/rke2/bin/kubectl --kubeconfig /etc/rancher/rke2/rke2.yaml get pods -A
```
Use helm repo add command to add the Helm chart repository that contains charts to install Rancher. For more information about the repository choices and which is best for your use case, see Choosing a Rancher Version.
```
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
```
We'll need to define a Kubernetes namespace where the resources created by the Chart should be installed. This should always be cattle-system:
```
kubectl create namespace cattle-system
```
This step is only required to use certificates issued by Rancher's generated CA (ingress.tls.source=rancher) or to request Let's Encrypt issued certificates (ingress.tls.source=letsEncrypt):
```
# If you have installed the CRDs manually, instead of setting `installCRDs` or `crds.enabled` to `true` in your Helm install command, you should upgrade your CRD resources before upgrading the Helm chart:
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/<VERSION>/cert-manager.crds.yaml

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```
Once you’ve installed cert-manager, you can verify it is deployed correctly by checking the cert-manager namespace for running pods:
```
kubectl get pods --namespace cert-manager
```
The default is for Rancher to generate a CA and uses cert-manager to issue the certificate for access to the Rancher server interface.
Because rancher is the default option for ingress.tls.source, we are not specifying ingress.tls.source when running the helm install command.
- Set the hostname to the DNS name you pointed at your load balancer.
- Set the bootstrapPassword to something unique for the admin user.
- To install a specific Rancher version, use the --version flag, example: --version 2.7.0
- For Kubernetes v1.25 or later, set global.cattle.psp.enabled to false when using Rancher v2.7.2-v2.7.4. This is not necessary for Rancher v2.7.5 and above, but you can still manually set the option if you choose.
```
helm install rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=your-dns \
  --set bootstrapPassword=admin \
  --set replicas=1
```
Wait for Rancher to be rolled out:
```
kubectl -n cattle-system rollout status deploy/rancher
kubectl -n cattle-system get deploy rancher
```

