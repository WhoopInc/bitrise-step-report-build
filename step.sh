#!/bin/bash
set -ex

python send.py
if [ $? != 0 ];
then
    echo "exit 1"
fi
echo "exit 0"