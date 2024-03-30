#!/bin/bash

python b.py $1
exit_code=$?

# move right if successful
if [ $exit_code -eq 0 ]; then
    osascript ctrl_right.applescript
    exit 0
fi


