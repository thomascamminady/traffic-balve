#!/bin/bash

POETRY_PATH=/Users/thomascamminady/.local/bin/poetry
SCRIPT_PATH=/Users/thomascamminady/Repos/traffic_balve/traffic_balve/save_distance_matrix.py
LOG_FILE=/Users/thomascamminady/Repos/traffic_balve/cron.log

echo "##################################################################" >> $LOG_FILE
echo "Running script at $(date)" >> $LOG_FILE
cd /Users/thomascamminady/Repos/traffic_balve
$POETRY_PATH run python $SCRIPT_PATH >> $LOG_FILE 2>&1
