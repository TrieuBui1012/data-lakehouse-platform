#!/usr/bin/env python
# -- coding: utf-8 --

# you can specify the column order if the column order in dest table
# is different from the original data columns.
# directly set the original columns in the array
# if empty or not set for a table, it will keep original
tpch_columns = {
    "customer": ["c_custkey",
                 "c_name",
                 "c_address",
                 "c_nationkey",
                 "c_phone",
                 "c_acctbal",
                 "c_mktsegment",
                 "c_comment",
                 "not_use_column"],
    "lineitem": ["l_orderkey",
                 "l_partkey",
                 "l_suppkey",
                 "l_linenumber",
                 "l_quantity",
                 "l_extendedprice",
                 "l_discount",
                 "l_tax",
                 "l_returnflag",
                 "l_linestatus",
                 "l_shipdate",
                 "l_commitdate",
                 "l_receiptdate",
                 "l_shipinstruct",
                 "l_shipmode",
                 "l_comment",
                 "not_use_column"],
    "nation": ["n_nationkey",
               "n_name",
               "n_regionkey",
               "n_comment",
               "not_use_column"],
    "orders": ["o_orderkey",
               "o_custkey",
               "o_orderstatus",
               "o_totalprice",
               "o_orderdate",
               "o_orderpriority",
               "o_clerk",
               "o_shippriority",
               "o_comment",
               "not_use_column"],
    "part": ["p_partkey",
             "p_name",
             "p_mfgr",
             "p_brand",
             "p_type",
             "p_size",
             "p_container",
             "p_retailprice",
             "p_comment",
             "not_use_column"],
    "partsupp": ["ps_partkey",
                 "ps_suppkey",
                 "ps_availqty",
                 "ps_supplycost",
                 "ps_comment",
                 "not_use_column"],
    "region": ["r_regionkey",
               "r_name",
               "r_comment",
               "not_use_column"],
    "supplier": ["s_suppkey",
                 "s_name",
                 "s_address",
                 "s_nationkey",
                 "s_phone",
                 "s_acctbal",
                 "s_comment",
                 "not_use_column"]
}

columns = {
    "tpch": tpch_columns
}
