#!/usr/bin/env bash

cd /proc
for pid in [0-9]*
do
  echo "PID = $pid with $(ls /proc/$pid/fd/ | wc -l) file descriptors"
done