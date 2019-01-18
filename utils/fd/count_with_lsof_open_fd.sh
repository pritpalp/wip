#!/usr/bin/env bash
sudo lsof -PMlnFKc -d '^cwd,^err,^ltx,^mem,^mmap,^pd,^rtd,^txt' |
  awk '
   function process() {
     if (pid || tid) {
       print n, \
             tid ? tid " (thread of " pid ": " pname")" : pid, \
             name
       n = tid = 0
     }
   }
   {value = substr($0, 2)}
   /^p/ {
     process()
     pid = value
     next
   }
   /^K/ {
     tid = value
     next
   }
   /^c/ {
      name = value
      if (!tid)
        pname = value
      next
   }
   /^f[0-9]/ {n++}
   END {process()}' | sort -rn