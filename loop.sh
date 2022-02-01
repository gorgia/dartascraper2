#!/bin/bash

python3 main.py

WAKEUP="03:00" # Wake up at this time tomorrow and run a command
while :
do
    SECS=$(expr `date -d "tomorrow $WAKEUP" +%s` - `date -d "now" +%s`)
    echo "`date +"%Y-%m-%d %T"`| Will sleep for $SECS seconds."
    sleep $SECS &  # We sleep in the background to make the screipt interruptible via SIGTERM when running in docker
    wait $!
    echo "`date +"%Y-%m-%d %T"`| Waking up"
    # Run your command here
    python3 main.py
done