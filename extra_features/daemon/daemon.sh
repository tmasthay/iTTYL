#!/bin/bash

REPO_ROOT=$(git rev-parse --show-toplevel)
AT_ROOT=$(python -c "print('1' if '$REPO_ROOT' == '$(pwd)' else '0')")
if [ $AT_ROOT -eq 0 ]; then
    echo "Please run this cron-like daemon from the root of the repository."
    exit 1
fi

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
    python extra_features/iphone_integration/sync_notes.py
    python send_scheduled_messages.py
    # If not the last iteration, then sleep
    if [ $i -lt $ITERATIONS ]; then
        # echo "Sleeping for $SLEEP_DURATION_MINUTES minutes..."
        sleep $SLEEP_DURATION_SECONDS
    fi
done
echo "Completed all iterations."
