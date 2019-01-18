import os
import resource

print "Open file limits (soft, hard):", resource.getrlimit(resource.RLIMIT_NOFILE)

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
  try:
    #print pid
    pid = pid.strip()
    process = os.popen("readlink /proc/" + pid + "/fd/*")
    cmd = open("/proc/" + pid + "/cmdline").read()
    fds = process.read().strip().splitlines()
    i = 0
    for fd in fds:
      if not (fd.startswith("socket") or fd.startswith("pipe") or fd.startswith("/dev/")):
        i = i + 1
    if i > 0:
      print (i, pid, cmd)
  except IOError:  # proc has already terminated
    continue