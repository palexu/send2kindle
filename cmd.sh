#!/bin/bash
/etc/init.d/cron start &&

# just keep this script running
while [[ true ]]; do
    sleep 1
done
