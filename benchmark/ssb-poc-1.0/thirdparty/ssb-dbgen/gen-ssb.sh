#!/bin/bash

set -e

BIN_PATH=`dirname "$0"`
BIN_PATH=`cd "${BIN_PATH}"; pwd`


function ceil(){
  echo "======================================"
  echo "need sudo privilege to install bc tool"
  echo "======================================"
  sudo yum install -y bc || echo "echo install yc error" && exit 0
  floor=`echo "scale=0;$1/1"|bc -l ` 
  add=`awk -v num1=$floor -v num2=$1 'BEGIN{print(num1<num2)?"1":"0"}'`
  echo `expr $floor  + $add`
}

#echo $BIN_PATH
#echo $PWD

if [ "$1" = "" ]; then
    echo "No scale factor provided. Using scale factor 1."
    echo "To use another scale factor use $0 X where X is an integer value between 1 and 1000"
    SIZE=1
else
    SIZE=$1
fi

if [ "$2" = "" ]; then
    echo "No table path provided, Using $PWD"
    TABLE_DIR=$PWD
else
    TABLE_DIR=$2
fi

if [ ! -d ${TABLE_DIR} ]; then
    mkdir -p ${TABLE_DIR}
fi

if [[ $SIZE -ge 1 ]] && [[ $SIZE -le 1000 ]];then
    if [[ $SIZE == "1" ]];then
        space="600M"
        generate_time="1 minutes"
    elif [[ $SIZE == "10" ]];then
        space="6G"
        generate_time="2 minutes"
    elif [[ $SIZE == "100" ]];then
        space="60G"
        generate_time="20 minutes"
    elif [[ $SIZE == "1000" ]];then
        space="600G"
        generate_time="3 hours"
    fi
    echo "Generating new data set of scale factor $SIZE, make sure current directory has more than $space disk space, which will take about $generate_time"
else
    echo "Wrong $SIZE scale factor"
    exit 1
fi

export DSS_CONFIG=${BIN_PATH}/../share/ssb-dbgen
export DSS_PATH=${TABLE_DIR}

if [ -e ${TABLE_DIR}/supplier.tbl ]; then
    echo "Backing up existing data set"
    TS=$(date '+%s')
    BACKUPDIR=${TABLE_DIR}/"backup.$TS"
    mkdir $BACKUPDIR
    mv ${TABLE_DIR}/*.tbl* $BACKUPDIR
    echo "Backup completed"
fi

echo -n "Begin generate lineorder table..."
${BIN_PATH}/dbgen -s $SIZE -i `ceil $SIZE` -T l && echo "completed!"
echo -n "Begin generate cutomers table..."
${BIN_PATH}/dbgen -s $SIZE -T c > /dev/null && echo "completed!"
echo -n "Begin generate date table..."
${BIN_PATH}/dbgen -s $SIZE -T d > /dev/null && echo "completed!"
echo -n "Begin generate parts table..."
${BIN_PATH}/dbgen -s $SIZE -T p > /dev/null && echo "completed!"
echo -n "Begin generate suppliers table..."
${BIN_PATH}/dbgen -s $SIZE -T s > /dev/null && echo "completed!"

echo "Data generation completed!"

du -sh ${TABLE_DIR}/*.tbl*
