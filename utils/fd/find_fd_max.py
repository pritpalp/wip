import os

p = os.popen("cat /proc/sys/fs/file-max")
q = int(p.read())
print "Max file descriptors: ", q

r = os.popen("lsof | wc -l")
s = int(r.read())
print "Open file decsriptors: ", s

t = float(s) / q * 100

print "Percentage fd in use: ", round(t, 2)