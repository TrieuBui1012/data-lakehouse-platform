create table household_demographics
(
    hd_demo_sk                integer  not null,
    hd_income_band_sk         integer  not null,
    hd_buy_potential          char(15) not null,
    hd_dep_count              integer  not null,
    hd_vehicle_count          integer  not null
)
duplicate key (hd_demo_sk)
distributed by hash(hd_demo_sk) buckets 1
properties(
    "replication_num" = "1"
);