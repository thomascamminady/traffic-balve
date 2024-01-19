#!/bin/bash

REPO_DIR="/Users/thomascamminadywahoo/Repos/traffic_balve"
LOG_FILE="/Users/thomascamminadywahoo/Repos/traffic_balve/.gitpush.log"
GIT_PATH="/opt/homebrew/bin/git"
GIT_LFS_PATH="/opt/homebrew/bin/git-lfs"
export PATH=$PATH:$GIT_LFS_PATH


# Start the log
echo "Starting git push at $(date)" >> "$LOG_FILE"

# Change into the repository directory
cd "$REPO_DIR" || exit

# Execute git push and log the output
{
    echo "Changing into directory: $(pwd)"
    echo "Running git push..."
    $GIT_PATH push
} >> "$LOG_FILE" 2>&1

# End the log
echo "Git push completed at $(date)" >> "$LOG_FILE"
