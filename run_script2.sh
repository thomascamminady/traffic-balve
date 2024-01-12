#!/bin/bash

# Navigate to the script's directory
cd /Users/thomascamminady/Repos/traffic_balve

CURRENT_TIMESTAMP=$(date)
GIT_COMMIT_MSG="Adding data at date $CURRENT_TIMESTAMP."
git commit -am "$GIT_COMMIT_MSG"
git push
