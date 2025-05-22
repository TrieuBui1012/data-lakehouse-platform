create table inventory
(
    inv_item_sk               integer               not null,
    inv_date_sk               integer               not null,
    inv_warehouse_sk          integer               not null,
    inv_quantity_on_hand      integer
)
duplicate key (inv_item_sk, inv_date_sk, inv_warehouse_sk)
distributed by hash(inv_item_sk) buckets 32
properties(
    "replication_num" = "1"
);