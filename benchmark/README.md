# Benchmark
**Requirement: Using centOS**
***I used CentOS-7.9 with 6 CPU | 6 GB RAM | 20 GB SSD***
1. Mount folders from s3 buckets
```
# 1. Enable EPEL repo (for s3fs)
sudo yum install -y epel-release

# 2. Install s3fs-fuse
sudo yum install -y s3fs-fuse

# 3. Store your credentials (owner‐read/write only)
echo ACCESS_KEY_ID:SECRET_ACCESS_KEY > /root/.passwd-s3fs
chmod 600 /root/.passwd-s3fs

# 4. Create mount points for each dataset
sudo mkdir -p /mnt/ssb
sudo mkdir -p /mnt/tpch
sudo mkdir -p /mnt/tpcds

# 5. Mount each bucket (replace BUCKET_NAME and, if non-AWS, add "-o url=<ENDPOINT>" e.g. MinIO)
sudo s3fs ssb /mnt/ssb         -o passwd_file=/root/.passwd-s3fs,url=https://s3.cloudfly.vn,use_path_request_style
sudo s3fs tpch /mnt/tpch       -o passwd_file=/root/.passwd-s3fs,url=https://s3.cloudfly.vn,use_path_request_style
sudo s3fs tpcds /mnt/tpcds     -o passwd_file=/root/.passwd-s3fs,url=https://s3.cloudfly.vn,use_path_request_style

# 6. Verify
df -h | grep s3fs
```
2. Generate data
```
wget https://starrocks-public.oss-cn-zhangjiakou.aliyuncs.com/ssb-poc-1.0.zip
unzip ssb-poc-1.0.zip
cd ssb-poc-1.0/
make && make install
cd output/

sh bin/gen-ssb.sh 100 /mnt/ssb

wget https://starrocks-public.oss-cn-zhangjiakou.aliyuncs.com/tpch-poc-1.0.zip
unzip tpch-poc-1.0
cd tpch-poc-1.0

sh bin/gen_data/gen-tpch.sh 100 /mnt/tpch

wget https://starrocks-public.oss-cn-zhangjiakou.aliyuncs.com/tpcds-poc-1.0.zip
unzip tpcds-poc-1.0
cd tpcds-poc-1.0

sh bin/gen_data/gen-tpcds.sh 100 /mnt/tpcds
```