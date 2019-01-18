#!/usr/bin/env bash
# pid count cmd
ps aux | sed 1d | awk '{print "fd_count=$(lsof -p " $2 " | wc -l) && echo " $2 " $fd_count " $11""}' | xargs -I {} bash -c