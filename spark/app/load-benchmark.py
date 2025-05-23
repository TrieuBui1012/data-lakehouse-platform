from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, current_timestamp

spark = (
    SparkSession.builder
        .appName("Load Benchmark")
        .getOrCreate()
)

def write_tables_to_hudi(catalog, database, tables, keys_mapping, database_target, base_path):
    for table in tables:
        path = f"{base_path}/{database_target}/{table}"
        df = spark.sql(f"SELECT * FROM {catalog}.{database}.{table}")
        
        (
           df.write.format("hudi")
           .option('hoodie.table.name', table)
           .option("hoodie.datasource.write.operation","insert_overwrite_table")
           .option("hoodie.datasource.write.secondarykey.column", ",".join(keys_mapping[table]))
           .option("hoodie.datasource.write.hive_style_partitioning", "true")
           .option("hoodie.datasource.hive_sync.enable", "true")
           .option("hoodie.datasource.hive_sync.mode", "hms")
           .option("hoodie.datasource.hive_sync.database", database_target)
           .option("hoodie.datasource.hive_sync.table", table)
           .option("hoodie.datasource.hive_sync.partition_extractor_class", "org.apache.hudi.hive.MultiPartKeysValueExtractor")
           .option("hoodie.datasource.hive_sync.metastore.uris", spark.conf.get("spark.hive.metastore.uris"))
           .mode("overwrite")
           .save(path)
        )

tpch_tables = [
    "customer",
    "lineitem",
    "nation",
    "orders",
    "part",
    "partsupp",
    "region",
    "supplier",]

tpch_keys_mapping = {
    "customer": ["c_custkey"],
    "lineitem": ["l_shipdate", "l_orderkey"],
    "nation": ["n_nationkey"],
    "orders": ["o_orderkey", "o_orderdate"],
    "part": ["p_partkey"],
    "partsupp": ["ps_partkey"],
    "region": ["r_regionkey"],
    "supplier": ["s_suppkey"]
}

tpcds_tables = [
    "call_center",
    "catalog_page",
    "catalog_returns",
    "catalog_sales",
    "customer_address",
    "customer_demographics",
    "customer",
    "date_dim",
    "household_demographics",
    "income_band",
    "inventory",
    "item",
    "promotion",
    "reason",
    "ship_mode",
    "store",
    "store_returns",
    "store_sales",
    "time_dim",
    "warehouse",
    "web_page",
    "web_returns",
    "web_sales",
    "web_site"
]

tpcds_keys_mapping = {
    "call_center": ["cc_call_center_sk"],
    "catalog_page": ["cp_catalog_page_sk"],
    "catalog_returns": ["cr_item_sk", "cr_order_number"],
    "catalog_sales": ["cs_item_sk", "cs_order_number"],
    "customer_address": ["ca_address_sk"],
    "customer_demographics": ["cd_demo_sk"],
    "customer": ["c_customer_sk"],
    "date_dim": ["d_date_sk"],
    "household_demographics": ["hd_demo_sk"],
    "income_band": ["ib_income_band_sk"],
    "inventory": ["inv_item_sk", "inv_date_sk", "inv_warehouse_sk"],
    "item": ["i_item_sk"],
    "promotion": ["p_promo_sk"],
    "reason": ["r_reason_sk"],
    "ship_mode": ["sm_ship_mode_sk"],
    "store": ["s_store_sk"],
    "store_returns": ["sr_item_sk", "sr_ticket_number"],
    "store_sales": ["ss_item_sk", "ss_ticket_number"],
    "time_dim": ["t_time_sk"],
    "warehouse": ["w_warehouse_sk"],
    "web_page": ["wp_web_page_sk"],
    "web_returns": ["wr_item_sk", "wr_order_number"],
    "web_sales": ["ws_item_sk", "ws_order_number"],
    "web_site": ["web_site_sk"]
}

base_path = "s3a://lakehouse"

write_tables_to_hudi(catalog="tpch", database="sf10", tables=tpch_tables, keys_mapping=tpch_keys_mapping, database_target="tpch_hudi", base_path=base_path)
write_tables_to_hudi(catalog="tpcds", database="sf10", tables=tpcds_tables, keys_mapping=tpcds_keys_mapping, database_target="tpcds_hudi", base_path=base_path)

spark.stop()
