#!/bin/bash
set -exv

echo "Running python script"
pwd
ls
echo $(pwd)
echo $(ls)

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${CURR_DIR}"

pwd
ls
echo $(pwd)
echo $(ls)

python ./send.py
if [ $? != 0 ];
then
    echo "exit 1"
fi
echo "exit 0"