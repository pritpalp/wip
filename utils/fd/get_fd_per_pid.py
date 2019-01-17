import os
import resource

print "Open file limits (soft, hard):", resource.getrlimit(resource.RLIMIT_NOFILE)

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
  try:
    print pid
    pid = pid.strip()
    process = os.popen("readlink /prod/" + pid + "/fd/*")
    print (process.read())
  except IOError:  # proc has already terminated
    continue