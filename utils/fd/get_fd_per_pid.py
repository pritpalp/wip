import os
import resource
import argparse

# needs to run as sudo/root to check all process

# Pull an argument to get the percentage limit you want to compare to, defaults to 80
parser = argparse.ArgumentParser()
parser.add_argument("-p", dest="percent_limit", default=80, type=int)
args = parser.parse_args()
percent_limit = args.percent_limit

# print "Open file descriptors from /proc/sys/fs/file-nr: ", open("/proc/sys/fs/file-nr").read().strip()
file_nr = open("/proc/sys/fs/file-nr").read().strip()
open_fd = file_nr.split()[0]
max_fd = file_nr.split()[-1]
percentage_max_fd = round(float(open_fd) / float(max_fd) * 100, 2)
if percentage_max_fd > percent_limit:
  print "Total open file descriptors have reached", percentage_max_fd, "% of the system max (", open_fd, " of ", max_fd, ")"

# get the soft limit and store it
soft_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[0]

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
  try:
    pid = pid.strip()
    cmd = open("/proc/" + pid + "/cmdline").read()  # get the cmd that's running
    # just try to grab the first part of the cmd
    if cmd.strip():
      cmd = cmd.split()[0]
      if ":" in cmd:
        cmd = cmd.split(":")[0]
      else:
        cmd = cmd.split("/")[-1]
    # cmd = os.readlink("/proc/" + pid + "/exe")  # this doesn't work very well, can get permission denied
    # path, cmd = os.path.split(cmd)
    # process = os.popen("readlink /proc/" + pid + "/fd/*")
    # fds = process.read().strip().splitlines()  # list the contents of /proc/[pid]/fd/
    # above code can also get permission denied, so eventually used os.walk() to get the names
    fds = []
    for (dirpath, dirname, filenames) in os.walk("/proc/" + pid + "/fd/"):
      fds.extend(filenames)
      break
    i = 0
    for fd in fds:
      if not (fd.startswith("socket") or fd.startswith("pipe")):
        i += 1  # we don't want to count everything
    if i > 0:
      percentage_used = round(float(i) / soft_limit * 100, 2)
      # only print out values if nearing the limit
      if percentage_used > percent_limit:
        print "PID ", pid, " (", cmd, ") has used", percentage_used, "% of the available file descriptors (", i, "/", soft_limit, ")"
  except IOError:  # proc has already terminated
    continue
