#!/bin/bash

set -e

BIN_PATH=`dirname "$0"`
BIN_PATH=`cd "${BIN_PATH}"; pwd`
CONF_FILE=${BIN_PATH}/../conf/starrocks.conf

QUERY_NAME=(Q1.1 Q1.2 Q1.3 Q2.1 Q2.2 Q2.3 Q3.1 Q3.2 Q3.3 Q3.4 Q4.1 Q4.2 Q4.3)
QUERY_NUM=0
TRIES=3
touch result.csv
truncate -s0 result.csv

fe_ip=`cat ${CONF_FILE} | grep mysql_host | sed 's/ //g' | awk -F ':' '{print $2}'`
fe_port=`cat ${CONF_FILE} | grep mysql_port | sed 's/ //g' | awk -F ':' '{print $2}'`
password=`cat ${CONF_FILE} | grep mysql_password | sed 's/ //g' | awk -F ':' '{print $2}'`
database=`cat ${CONF_FILE} | grep database | sed 's/ //g' | awk -F ':' '{print $2}'`
export MYSQL_PWD=$password

if [[ $1 == "" ]];then
    echo "Need to specify whether to test single or multiple tables, for example: ssb-flat"
    exit 1
else
    query_file=${BIN_PATH}/../share/ssb_test/sql/query/single-file-${1}.sql
fi

Total=0
echo -e "SQL\tTime(ms)" | tee -a result.csv
while read -r query; do
    sync
    echo -ne "${QUERY_NAME[$QUERY_NUM]}\t" | tee -a result.csv
    # warm up 3 times
    for i in {1..3}; do
        mysql -vvv -h${fe_ip} -P${fe_port} -uroot ${database} -e "${query}" > /dev/null 2>&1
    done

    # execute $TRIES times and take the average
    TRIES_TIME=0
    TRIES_TIME_AVG=0
    for i in $(seq 1 $TRIES); do
        RES=$(mysql -vvv -h${fe_ip} -P${fe_port} -uroot ${database} -e "${query}" | perl -nle 'print $1 if /\((\d+\.\d+)+ sec\)/' ||:)
        TRIES_TIME=`echo "$TRIES_TIME + $RES" | bc`
    done
    TRIES_TIME=`echo "$TRIES_TIME * 1000" | bc`
    TRIES_TIME_AVG=`echo "$TRIES_TIME/$TRIES"| bc`
    echo -n "${TRIES_TIME_AVG}" | tee -a result.csv

    Total=`echo "${Total} + ${TRIES_TIME_AVG}" | bc`
    echo "" | tee -a result.csv

    QUERY_NUM=$((QUERY_NUM + 1))
done < ${query_file}
echo -e "Total\t$Total" | tee -a result.csv
