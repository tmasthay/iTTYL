#!/bin/bash

date 

# Get the folder containing the script
folder=$(dirname "$0")

# Use cd and pwd to get an absolute path
project_root=$(cd "$folder/../.." && pwd)

# Define idle time threshold (e.g., 300 seconds = 5 minutes)
idle_threshold=300

# Get the current idle time in seconds
idle_time=$(ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}')

/Users/tylermasthay/anaconda3/bin/python extra_features/sync_notes/sync_notes.py 
/Users/tylermasthay/anaconda3/bin/python send_scheduled_messages.py 

# Check if the computer has been idle for longer than the threshold
if (( $(echo "$idle_time > $idle_threshold" | bc -l) )); then
    echo "The system is idle. Running script and going back to sleep."
    pmset sleepnow
else
    echo "The system is active. Only running the script."
    # Place your script's commands here
fi
