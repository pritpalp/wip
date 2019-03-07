#!/usr/bin/python

import os
import resource
import argparse

# needs to run as sudo/root to check all process

# Pull an argument to get the percentage limit you want to compare to, defaults to 80
parser = argparse.ArgumentParser(description='Get the open file descriptors per process '
                                             'and print a messaage when its above a specified threshold')
parser.add_argument("-p", dest="percent_limit", default=80,
                    help='Percentage to compare the file descriptor usage to, defaults to 80', type=int)
args = parser.parse_args()
# print out usage if incorrect arguments are passed
if not vars(args):
  parser.print_help()
  parser.exit(1)
percent_limit = args.percent_limit

# Pull the max open fd's and currently open fd's
file_nr = open("/proc/sys/fs/file-nr").read().strip()
open_fd = file_nr.split()[0]
max_fd = file_nr.split()[-1]
percentage_max_fd = round(float(open_fd) / float(max_fd) * 100, 2)
if percentage_max_fd > percent_limit:
  print "Total open file descriptors have reached", percentage_max_fd, "% of the system max (", open_fd, " of ", max_fd, ")"

# get the soft limit and store it, to use as backup
default_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[0]

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
  try:
    pid = pid.strip()
    soft_limit = default_limit
    limits = open("/proc/" + pid + "/limits").readlines()  # get the limits for the proc
    for line in limits:
      if line.startswith("Max open files"):
        soft_limit = int(line.split()[3])  # splitting the line on spaces we want the 4th value
        break
    # used os.walk() to get the names in the /proc/[pid]/fd dir
    fds = []
    for (dirpath, dirname, filenames) in os.walk("/proc/" + pid + "/fd/"):
      fds.extend(filenames)
      break
    i = 0
    for fd in fds:
      if not (fd.startswith("socket") or fd.startswith("pipe")):
        i += 1  # we don't want to count everything, can ignore sockets and pipes
    if i > 0:
      percentage_used = round(float(i) / soft_limit * 100, 2)
      # only print out values if nearing the limit
      if percentage_used > percent_limit:
        print "PID ", pid, " has used", percentage_used, "% of the available file descriptors (", i, "/", soft_limit, ")"
  except IOError:  # proc has already terminated
    continue
  except ZeroDivisionError: # somehow managed to get a zero, ignore for now
    continue
