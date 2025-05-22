# Installing Longhorn with Rancher
1. Fulfill all Installation Requirements.
2. Go to the cluster where you want to install Longhorn.
3. Click Apps.
4. Click Charts.
5. Click Longhorn.
6. Optional: To customize the initial settings, click Longhorn Default Settings and edit the configuration. For help customizing the settings, refer to the Longhorn documentation.
7. Click Install.
**Result**: Longhorn is deployed in the Kubernetes cluster.

# Accessing Longhorn from the Rancher UI
1. Go to the cluster where Longhorn is installed. In the left navigation menu, click Longhorn.
2. On this page, you can edit Kubernetes resources managed by Longhorn. To view the Longhorn UI, click the Longhorn button in the Overview section.
**Result**: You will be taken to the Longhorn UI, where you can manage your Longhorn volumes and their replicas in the Kubernetes cluster, as well as secondary backups of your Longhorn storage that may exist in another Kubernetes cluster or in S3.

*Reference: https://ranchermanager.docs.rancher.com/integrations-in-rancher/longhorn/overview*
