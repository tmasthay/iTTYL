#!/bin/bash

# Sleep duration in minutes (provided by the user)
SLEEP_DURATION_MINUTES=${1:-5}

# Convert sleep duration to seconds
SLEEP_DURATION_SECONDS=$((SLEEP_DURATION_MINUTES * 60))

# Calculate the number of iterations needed to run approximately 24 hours
# There are 1440 minutes in 24 hours, 1440*7 \approx 10,000
ITERATIONS=$((10000 / SLEEP_DURATION_MINUTES))

echo "Starting the script with sleep duration of $SLEEP_DURATION_MINUTES minutes for a total of $ITERATIONS iterations..."

for (( i=1; i<=ITERATIONS; i++ ))
do
    echo "Iteration $i of $ITERATIONS of $SLEEP_DURATION_MINUTES minutes each"
    python tmp.py
    python send_scheduled_messages.py
    # If not the last iteration, then sleep
    if [ $i -lt $ITERATIONS ]; then
        # echo "Sleeping for $SLEEP_DURATION_MINUTES minutes..."
        sleep $SLEEP_DURATION_SECONDS
    fi
done
echo "Completed all iterations."
