#!/bin/bash

# Navigate to the script's directory
cd /Users/thomascamminady/Repos/traffic_balve

echo "##########################################################GIT#################################################################" >> $LOG_FILE
# Log the current date and time
CURRENT_TIMESTAMP=$(date)
# Commit the changes
GIT_COMMIT_MSG="Adding data at date $CURRENT_TIMESTAMP."
git commit -am "$GIT_COMMIT_MSG"
git push
