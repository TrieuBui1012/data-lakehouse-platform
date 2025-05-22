# A data lakehouse platform
## Prepare cluster:
Run these command on each node (create a sh file to run):
```
# Modify the configuration file.
cat >> /etc/sysctl.conf << EOF
vm.overcommit_memory=1
EOF
# Bring the change into effect.
sysctl -p
# Change the configuration temporarily.
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/defrag
# Change the configuration permanently.
cat >> /etc/rc.d/rc.local << EOF
if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
   echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
fi
if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
   echo madvise > /sys/kernel/mm/transparent_hugepage/defrag
fi
EOF
chmod +x /etc/rc.d/rc.local
swapoff -a
free -m
# Modify the configuration file.
cat >> /etc/sysctl.conf << EOF
vm.swappiness=0
EOF
# Bring the change into effect.
sysctl -p
cat >> /etc/security/limits.conf << EOF
* soft nproc 65535
* hard nproc 65535
* soft nofile 655350
* hard nofile 655350
* soft stack unlimited
* hard stack unlimited
* hard memlock unlimited
* soft memlock unlimited
EOF

cat >> /etc/security/limits.d/20-nproc.conf << EOF 
*          soft    nproc     65535
root       soft    nproc     65535
EOF
# Modify the configuration file.
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_abort_on_overflow=1
EOF
# Bring the change into effect.
sysctl -p
# Modify the configuration file.
cat >> /etc/sysctl.conf << EOF
net.core.somaxconn=1024
EOF
# Bring the change into effect.
sysctl -p
# Modify the configuration file.
cat >> /etc/sysctl.conf << EOF
vm.max_map_count = 262144
EOF
# Bring the change into effect.
sysctl -p
echo 120000 > /proc/sys/kernel/threads-max
echo 200000 > /proc/sys/kernel/pid_max
sudo apt-get update
sudo apt-get install chrony
sudo systemctl enable --now chrony
```
## Configure netplan if neccessary:
```
sudo nano /etc/netplan/01-netcfg.yaml
```
Configure and save this:
```
network:
  version: 2
  ethernets:
    ens3:
      dhcp4: true
    ens8:
      dhcp4: no
      addresses:
        - 192.168.1.97/24
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```
```
sudo netplan apply
```