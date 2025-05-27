create table customer_demographics
(
    cd_demo_sk                integer  not null,
    cd_gender                 char(1)  not null,
    cd_marital_status         char(1)  not null,
    cd_education_status       char(20) not null,
    cd_purchase_estimate      integer  not null,
    cd_credit_rating          char(10) not null,
    cd_dep_count              integer  not null,
    cd_dep_employed_count     integer  not null,
    cd_dep_college_count      integer  not null
)
duplicate key (cd_demo_sk)
distributed by hash(cd_demo_sk) buckets 10
properties(
    "replication_num" = "1"
);