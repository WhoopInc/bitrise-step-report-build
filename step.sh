#!/bin/bash
set -exv

echo 'cd-ing to step directory'
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${CURR_DIR}"

echo 'installing dependencies'
pip3 install requests

echo 'listing time metrics'
echo "${STARTED_AT}"
echo "${COMPLETED_AT}"
echo "${TOTAL_DURATION}"
echo ${$BITRISE_GIT_MESSAGE}
echo $BITRISE_GIT_MESSAGE
echo "$BITRISE_GIT_MESSAGE"

echo 'executing script'
python3 ./send.py

if [ $? != 0 ];
then
  echo "FAILURE"
  echo "exit 1"
fi
echo "SUCCESSFUL"
echo "exit 0"