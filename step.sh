#!/bin/bash
set -exv

echo 'cd-ing to step directory'
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${CURR_DIR}"

echo 'installing dependencies'
pip3 install requests

echo 'executing script'
python3 ./send.py

exit 1
if [ $? != 0 ];
then
  echo "FAILURE"
  exit 1
fi
echo "SUCCESSFUL"
exit 0