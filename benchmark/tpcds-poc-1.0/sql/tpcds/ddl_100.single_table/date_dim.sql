create table date_dim
(
    d_date_sk                 integer   not null,
    d_date_id                 char(16)  not null,
    d_date                    date      not null,
    d_month_seq               integer   not null,
    d_week_seq                integer   not null,
    d_quarter_seq             integer   not null,
    d_year                    integer   not null,
    d_dow                     integer   not null,
    d_moy                     integer   not null,
    d_dom                     integer   not null,
    d_qoy                     integer   not null,
    d_fy_year                 integer   not null,
    d_fy_quarter_seq          integer   not null,
    d_fy_week_seq             integer   not null,
    d_day_name                char(9)   not null,
    d_quarter_name            char(6)   not null,
    d_holiday                 char(1)   not null,
    d_weekend                 char(1)   not null,
    d_following_holiday       char(1)   not null,
    d_first_dom               integer   not null,
    d_last_dom                integer   not null,
    d_same_day_ly             integer   not null,
    d_same_day_lq             integer   not null,
    d_current_day             char(1)   not null,
    d_current_week            char(1)   not null,
    d_current_month           char(1)   not null,
    d_current_quarter         char(1)   not null,
    d_current_year            char(1)   not null
)
duplicate key (d_date_sk)
distributed by hash(d_date_sk) buckets 5
properties(
    "replication_num" = "1"
);