#!/bin/bash

# Define the path to the poetry executable and your script
POETRY_PATH=/Users/thomascamminadywahoo/.local/bin/poetry

# Define the log file location
LOG_FILE=/Users/thomascamminadywahoo/Repos/traffic_balve/cron.log

# Navigate to the script's directory
cd /Users/thomascamminadywahoo/Repos/traffic_balve

echo "####################################################################################################################################" >> $LOG_FILE
# Log the current date and time
CURRENT_TIMESTAMP=$(date)

CURRENT_TIMESTAMP=$(date)
GIT_COMMIT_MSG="Adding data at date $CURRENT_TIMESTAMP."

$POETRY_PATH run git commit -am "$GIT_COMMIT_MSG"
$POETRY_PATH run git push
