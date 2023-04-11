#!/bin/sh

set -e

echo "compile schemas"
for i in `ls schemas`
do
    echo $i
    ajv compile -s schemas/$i --validate-formats=false  -r definitions/*.json   
done
echo ""
echo "validate data with Influx schemas"
for i in `ls influxSchemas`
do
    echo $i
    ajv compile -s influxSchemas/$i --validate-formats=false  -r definitions/*.json   
done
echo ""
echo "validate data with Query schemas"
for i in `ls graphQuerySchema`
do
    echo $i
    ajv compile -s graphQuerySchema/$i --validate-formats=false  -r definitions/*.json   
done
echo ""
echo "validate data with schemas"

for i in `ls data/`
do
    ajv validate -s schemas/$i -d data/$i
done