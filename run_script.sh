#!/bin/bash

# Define the path to the poetry executable and your script
POETRY_PATH=/Users/thomascamminady/.local/bin/poetry
SCRIPT_PATH=/Users/thomascamminady/Repos/traffic_balve/traffic_balve/save_distance_matrix.py

# Define the log file location
LOG_FILE=/Users/thomascamminady/Repos/traffic_balve/cron.log

# Run the script and redirect both stdout and stderr to the log file
$POETRY_PATH run python $SCRIPT_PATH >> $LOG_FILE 2>&1
