#!/bin/bash
set -exv

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${CURR_DIR}"


python ./send.py
if [ $? != 0 ];
then
    echo "exit 1"
fi
echo "exit 0"