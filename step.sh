#!/bin/bash
set -exv

echo 'cd-ing to step directory'
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${CURR_DIR}"

pip install requests

echo 'running script'
python3 ./send.py

if [ $? != 0 ];
then
    echo "exit 1"
fi
echo "exit 0"