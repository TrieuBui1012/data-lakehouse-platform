drop table if exists part;
CREATE TABLE part  ( p_partkey          int NOT NULL,
                          p_name        VARCHAR(55) NOT NULL,
                          p_mfgr        VARCHAR(25) NOT NULL,
                          p_brand       VARCHAR(10) NOT NULL,
                          p_type        VARCHAR(25) NOT NULL,
                          p_size        int NOT NULL,
                          p_container   VARCHAR(10) NOT NULL,
                          p_retailprice decimal(15, 2) NOT NULL,
                          p_comment     VARCHAR(23) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`p_partkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`p_partkey`) BUCKETS 24
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT",
    "colocate_with" = "group_tpch_100p"
);