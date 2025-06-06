drop database if exists tpch;
create database tpch;
use tpch;

drop table if exists customer;
CREATE TABLE customer ( c_custkey     int NOT NULL,
                        c_name        VARCHAR(25) NOT NULL,
                        c_address     VARCHAR(40) NOT NULL,
                        c_nationkey   int NOT NULL,
                        c_phone       CHAR(15) NOT NULL,
                        c_acctbal     decimal(15, 2)   NOT NULL,
                        c_mktsegment  CHAR(10) NOT NULL,
                        c_comment     VARCHAR(117) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`c_custkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`c_custkey`) BUCKETS 24
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT"
);

drop table if exists lineitem;
CREATE TABLE lineitem ( l_orderkey    bigint NOT NULL,
                             l_linenumber  int not null,
                             l_shipdate    DATE NOT NULL,
                             l_partkey     int NOT NULL,
                             l_suppkey     int not null,
                             l_quantity    decimal(15, 2) NOT NULL,
                             l_extendedprice  decimal(15, 2) NOT NULL,
                             l_discount    decimal(15, 2) NOT NULL,
                             l_tax         decimal(15, 2) NOT NULL,
                             l_returnflag  CHAR(1) NOT NULL,
                             l_linestatus  CHAR(1) NOT NULL,
                             l_commitdate  DATE NOT NULL,
                             l_receiptdate DATE NOT NULL,
                             l_shipinstruct CHAR(25) NOT NULL,
                             l_shipmode     CHAR(10) NOT NULL,
                             l_comment      VARCHAR(44) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`l_orderkey`, `l_linenumber`, `l_shipdate`)
COMMENT "OLAP"
PARTITION BY RANGE(`l_shipdate`)
(
   START ("1992-01-01") END ("1999-01-01") EVERY (INTERVAL 1 year)
)
DISTRIBUTED BY HASH(`l_orderkey`) BUCKETS 48
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT",
    "colocate_with" = "group_tpch_1000"
);

drop table if exists nation;
CREATE TABLE `nation` (
  `n_nationkey` int(11) NOT NULL,
  `n_name`      char(25) NOT NULL,
  `n_regionkey` int(11) NOT NULL,
  `n_comment`   varchar(152) NULL
) ENGINE=OLAP
DUPLICATE KEY(`N_NATIONKEY`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`N_NATIONKEY`) BUCKETS 1
PROPERTIES (
    "replication_num" = "3",
    "in_memory" = "false",
    "storage_format" = "DEFAULT"
);

drop table if exists orders;
CREATE TABLE orders  ( o_orderkey       bigint NOT NULL,
                       o_orderdate      DATE NOT NULL,
                       o_custkey        int NOT NULL,
                       o_orderstatus    CHAR(1) NOT NULL,
                       o_totalprice     decimal(15, 2) NOT NULL,
                       o_orderpriority  CHAR(15) NOT NULL,
                       o_clerk          CHAR(15) NOT NULL,
                       o_shippriority   int NOT NULL,
                       o_comment        VARCHAR(79) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`o_orderkey`, `o_orderdate`)
COMMENT "OLAP"
PARTITION BY RANGE(`o_orderdate`)
(
   START ("1992-01-01") END ("1999-01-01") EVERY (INTERVAL 1 year)
)
DISTRIBUTED BY HASH(`o_orderkey`) BUCKETS 48
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT",
    "colocate_with" = "group_tpch_1000"
);

drop table if exists part;
CREATE TABLE part  ( p_partkey          int NOT NULL,
                          p_name        VARCHAR(55) NOT NULL,
                          p_mfgr        CHAR(25) NOT NULL,
                          p_brand       CHAR(10) NOT NULL,
                          p_type        VARCHAR(25) NOT NULL,
                          p_size        int NOT NULL,
                          p_container   CHAR(10) NOT NULL,
                          p_retailprice decimal(15, 2) NOT NULL,
                          p_comment     VARCHAR(23) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`p_partkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`p_partkey`) BUCKETS 24
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT"
);

drop table if exists partsupp;
CREATE TABLE partsupp ( ps_partkey          int NOT NULL,
                             ps_suppkey     int NOT NULL,
                             ps_availqty    int NOT NULL,
                             ps_supplycost  decimal(15, 2)  NOT NULL,
                             ps_comment     VARCHAR(199) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`ps_partkey`, `ps_suppkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`ps_partkey`) BUCKETS 96
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT"
);

drop table if exists region;
CREATE TABLE region  ( r_regionkey      int NOT NULL,
                            r_name       CHAR(25) NOT NULL,
                            r_comment    VARCHAR(152))
ENGINE=OLAP
DUPLICATE KEY(`r_regionkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`r_regionkey`) BUCKETS 1
PROPERTIES (
    "replication_num" = "3",
    "in_memory" = "false",
    "storage_format" = "DEFAULT"
);

drop table if exists supplier;
CREATE TABLE supplier (  s_suppkey       int NOT NULL,
                             s_name        CHAR(25) NOT NULL,
                             s_address     VARCHAR(40) NOT NULL,
                             s_nationkey   int NOT NULL,
                             s_phone       CHAR(15) NOT NULL,
                             s_acctbal     decimal(15, 2) NOT NULL,
                             s_comment     VARCHAR(101) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`s_suppkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`s_suppkey`) BUCKETS 12
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT"
);

drop table if exists revenue0;
create view revenue0 (supplier_no, total_revenue) as
        select
                l_suppkey,
                sum(l_extendedprice * (1 - l_discount))
        from
                lineitem
        where
                l_shipdate >= date '1996-01-01'
                and l_shipdate < date '1996-01-01' + interval '3' month
        group by
                l_suppkey;
