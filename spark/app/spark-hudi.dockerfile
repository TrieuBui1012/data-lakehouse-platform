FROM oci.stackable.tech/sdp/spark-k8s:3.5.5-stackable25.3.0

COPY ./conf/spark-defaults.conf /stackable/spark/conf/spark-defaults.conf

COPY ./conf/core-site.xml /stackable/spark/conf/core-site.xml

COPY ./jars/kyuubi-spark-connector-tpcds_2.12-1.10.1.jar /stackable/spark/jars/kyuubi-spark-connector-tpcds_2.12-1.10.1.jar

COPY ./jars/kyuubi-spark-connector-tpch_2.12-1.10.1.jar /stackable/spark/jars/kyuubi-spark-connector-tpch_2.12-1.10.1.jar

COPY ./jars/hudi-spark3.5-bundle_2.12-1.0.2.jar /stackable/spark/jars/hudi-spark3.5-bundle_2.12-1.0.2.jar

COPY load-benchmark.py /stackable/spark/myapp/load-benchmark.py
