#!/bin/sh -ex

# Start the crontab and run nginx
cron -f &
ps
nginx 
