from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id

spark = (
    SparkSession.builder
        .appName("Load Benchmark")
        .getOrCreate()
)

# 1) Định nghĩa mapping table → list các cột key
key_mapping = {
    # TPC-H
    "customer":       ["c_custkey"],
    "lineitem":       ["l_shipdate", "l_orderkey"],
    "nation":         ["n_nationkey"],
    "orders":         ["o_orderkey", "o_orderdate"],
    "part":           ["p_partkey"],
    "partsupp":       ["ps_partkey"],
    "region":         ["r_regionkey"],
    "supplier":       ["s_suppkey"],

    # TPC-DS (ví dụ một số bảng chính; bổ sung tương tự cho các bảng khác nếu cần)
    "call_center":              ["cc_call_center_sk"],
    "catalog_page":             ["cp_catalog_page_sk"],
    "catalog_returns":          ["cr_item_sk", "cr_order_number"],
    "catalog_sales":            ["cs_item_sk", "cs_order_number"],
    "customer_address":         ["ca_address_sk"],
    "customer_demographics":     ["cd_demo_sk"],
    "customer":                 ["c_customer_sk"],
    "date_dim":                 ["d_date_sk"],
    "household_demographics":   ["hd_demo_sk"],
    "income_band":              ["ib_income_band_sk"],
    "inventory":                ["inv_item_sk", "inv_date_sk", "inv_warehouse_sk"],
    "item":                     ["i_item_sk"],
    "promotion":                ["p_promo_sk"],
    "reason":                   ["r_reason_sk"],
    "ship_mode":                ["sm_ship_mode_sk"],
    "store_returns":            ["sr_item_sk", "sr_ticket_number"],
    "store_sales":              ["ss_item_sk", "ss_ticket_number"],
    "store":                    ["s_store_sk"],
    "time_dim":                 ["t_time_sk"],
    "warehouse":                ["w_warehouse_sk"],
    "web_page":                 ["wp_web_page_sk"],
    "web_returns":              ["wr_item_sk", "wr_order_number"],
    "web_sales":                ["ws_item_sk", "ws_order_number"],
    "web_site":                 ["web_site_sk"],
}

catalogs = ["tpch", "tpcds"]
sf_schema = "sf10"
base_path = "s3a://lakehouse/hudi"

for catalog in catalogs:
    db = f"{catalog}.{sf_schema}"
    tables = [t.name for t in spark.catalog.listTables(db)]
    print(f"Found {len(tables)} tables in {db}")

    for table in tables:
        full_name = f"{db}.{table}"
        print(f"→ Processing {full_name}")

        df = spark.table(full_name)

        # 2) Xác định key columns & precombine
        keys = key_mapping.get(table)
        if keys:
            recordkey = ",".join(keys)
            precombine = keys[0]
        else:
            # fallback: tạo uuid nếu chưa có mapping
            df = df.withColumn("uuid", monotonically_increasing_id())
            recordkey = "uuid"

        target_path = f"{base_path}/{catalog}/{table}"

        # 3) Viết Hudi
        if keys:
            (
                df.write
                    .format("hudi")
                    .mode("overwrite")
                    .option("hoodie.table.name", table)
                    .option("hoodie.datasource.write.operation", "bulk_insert")
                    .option("hoodie.datasource.write.recordkey.field", recordkey)
                    .option("hoodie.datasource.write.precombine.field", precombine)
                    .option("hoodie.datasource.hive_sync.enable", "true")
                    .option("hoodie.datasource.hive_sync.database", catalog)
                    .option("hoodie.datasource.hive_sync.table", table)
                    .option("hoodie.datasource.hive_sync.mode", "hms")
                    .option("hoodie.datasource.hive_sync.metastore.uris",
                            spark.conf.get("spark.hive.metastore.uris"))
                    .option("hoodie.datasource.hive_sync.support_timestamp", "true")
                    .save(target_path)
            )
        else:
            (
                df.write
                    .format("hudi")
                    .mode("overwrite")
                    .option("hoodie.table.name", table)
                    .option("hoodie.datasource.write.operation", "bulk_insert")
                    .option("hoodie.datasource.write.recordkey.field", recordkey)
                    .option("hoodie.datasource.write.keygenerator.class", "org.apache.hudi.keygen.NonpartitionedKeyGenerator")
                    .option("hoodie.datasource.hive_sync.enable", "true")
                    .option("hoodie.datasource.hive_sync.database", catalog)
                    .option("hoodie.datasource.hive_sync.table", table)
                    .option("hoodie.datasource.hive_sync.mode", "hms")
                    .option("hoodie.datasource.hive_sync.metastore.uris",
                            spark.conf.get("spark.hive.metastore.uris"))
                    .option("hoodie.datasource.hive_sync.support_timestamp", "true")
                    .save(target_path)
            )

        print(f"   ✓ Wrote Hudi table `{table}` with recordkey=[{recordkey}]")

spark.stop()
