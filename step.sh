#!/bin/bash
set -exv

echo 'cd-ing to step directory'
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${CURR_DIR}"

echo 'installing dependencies'
pip install requests

echo 'executing script'
python3 ./send.py

if [ $? != 0 ];
then
  echo "FAILURE"
  echo "exit 1"
fi
echo "SUCCESSFUL"
echo "exit 0"