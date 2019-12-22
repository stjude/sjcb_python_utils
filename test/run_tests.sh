#!/usr/bin/env bash

cd $(dirname ${0})

export PYTHONPATH=$(pwd)/../src:$PYTHONPATH
export PATH=$(pwd)/../scripts:$PATH

coverage run -m --source ../src/sjcb unittest discover unit_tests -p "*test.py" -b

coverage_report=$(mktemp)
coverage report -m > $coverage_report
cat $coverage_report
rm $coverage_report

