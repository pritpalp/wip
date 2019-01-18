import os
import resource

# needs to run as sudo/root to check all process
print "Open file limits (soft, hard):", resource.getrlimit(resource.RLIMIT_NOFILE)
print "Open file limit from /proc/sys/fs/file-max: ", open("/proc/sys/fs/file-max").read().strip()
print "Open file descriptors from /proc/sys/fs/file-nr: ", open("/proc/sys/fs/file-nr").read().strip()

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
  try:
    pid = pid.strip()
    process = os.popen("readlink /proc/" + pid + "/fd/*")
    cmd = open("/proc/" + pid + "/cmdline").read()
    fds = process.read().strip().splitlines()
    i = 0
    for fd in fds:
      if not (fd.startswith("socket") or fd.startswith("pipe") or fd.startswith("/dev/")):
        i += 1  # we don't want to count everything
    if i > 0:
      print (i, pid, cmd)
  except IOError:  # proc has already terminated
    continue