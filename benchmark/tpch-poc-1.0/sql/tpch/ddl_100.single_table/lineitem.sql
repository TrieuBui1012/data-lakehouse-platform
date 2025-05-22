drop table if exists lineitem;
CREATE TABLE lineitem ( l_shipdate    DATE NOT NULL,
                             l_orderkey    int NOT NULL,
                             l_linenumber  int not null,
                             l_partkey     int NOT NULL,
                             l_suppkey     int not null,
                             l_quantity    decimal(15, 2) NOT NULL,
                             l_extendedprice  decimal(15, 2) NOT NULL,
                             l_discount    decimal(15, 2) NOT NULL,
                             l_tax         decimal(15, 2) NOT NULL,
                             l_returnflag  VARCHAR(1) NOT NULL,
                             l_linestatus  VARCHAR(1) NOT NULL,
                             l_commitdate  DATE NOT NULL,
                             l_receiptdate DATE NOT NULL,
                             l_shipinstruct VARCHAR(25) NOT NULL,
                             l_shipmode     VARCHAR(10) NOT NULL,
                             l_comment      VARCHAR(44) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`l_shipdate`, `l_orderkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`l_orderkey`) BUCKETS 96
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT",
    "colocate_with" = "group_tpch_100"
);