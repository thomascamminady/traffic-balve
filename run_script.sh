#!/bin/bash

# Define the path to the poetry executable and your script
POETRY_PATH=/Users/thomascamminady/.local/bin/poetry
SCRIPT_PATH=/Users/thomascamminady/Repos/traffic_balve/traffic_balve/save_distance_matrix.py

# Define the log file location
LOG_FILE=/Users/thomascamminady/Repos/traffic_balve/cron.log

# Navigate to the script's directory
cd /Users/thomascamminady/Repos/traffic_balve

# Log the current date and time
CURRENT_TIMESTAMP=$(date)
echo "Running script at $CURRENT_TIMESTAMP" >> $LOG_FILE

# Run the script and redirect both stdout and stderr to the log file
$POETRY_PATH run python $SCRIPT_PATH >> $LOG_FILE 2>&1

# Adding new JSON files to the staging area
git add data/*.json

# Commit the changes
GIT_COMMIT_MSG="Adding data at date $CURRENT_TIMESTAMP"
git commit -am "$GIT_COMMIT_MSG"

# If commit fails, it might be due to pre-commit hooks making changes
if [ $? -ne 0 ]; then
    # Add any files modified by pre-commit hooks
    git add .

    # Attempt to commit again
    git commit -am "$GIT_COMMIT_MSG"

    if [ $? -ne 0 ]; then
        echo "Git commit failed after retry. Check the pre-commit hooks or other issues." >> $LOG_FILE
    else
        echo "Data committed successfully at $CURRENT_TIMESTAMP after retry" >> $LOG_FILE
    fi
else
    echo "Data committed successfully at $CURRENT_TIMESTAMP" >> $LOG_FILE
fi
