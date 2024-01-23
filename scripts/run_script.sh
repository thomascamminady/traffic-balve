#!/bin/bash

# Define the path to the poetry executable and your script
POETRY_PATH=/Users/thomascamminadywahoo/.local/bin/poetry
SCRIPT_PATH=/Users/thomascamminadywahoo/Repos/traffic_balve/traffic_balve/save_distance_matrix.py

# Define the log file location
LOG_FILE=/Users/thomascamminadywahoo/Repos/traffic_balve/scripts/.cron.log

# Navigate to the script's directory
cd /Users/thomascamminadywahoo/Repos/traffic_balve

echo "####################################################################################################################################" >> $LOG_FILE
# Log the current date and time
CURRENT_TIMESTAMP=$(date)
echo "Running script at $CURRENT_TIMESTAMP" >> $LOG_FILE

# Run the script and redirect both stdout and stderr to the log file
$POETRY_PATH run python $SCRIPT_PATH >> $LOG_FILE 2>&1


CURRENT_TIMESTAMP=$(date)
GIT_COMMIT_MSG="Adding data at date $CURRENT_TIMESTAMP."

$POETRY_PATH run git commit -am "$GIT_COMMIT_MSG" >> $LOG_FILE 2>&1
$POETRY_PATH run git push >> $LOG_FILE 2>&1
