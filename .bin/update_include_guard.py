#!/usr/bin/env python

import os
import sys

def UpdateGuard(file_path, new_guard):
  cont_lines = open(file_path).readlines()
  # find old_guard
  old_guard = ""
  for i in range(0, len(cont_lines) - 1):
    if cont_lines[i].startswith('#ifndef'):
      old_guard_candidate = cont_lines[i][7:].strip()
      if cont_lines[i+1].startswith('#define') == False:
        continue
      old_guard_check = cont_lines[i+1][7:].strip()
      if old_guard_candidate == old_guard_check:
        old_guard = old_guard_candidate
        break
  if old_guard == new_guard or old_guard == "":
    return
  # replace
  for i in range(0, len(cont_lines)):
    cont_lines[i] = cont_lines[i].replace(old_guard, new_guard)
  # write
  fp = open(file_path, 'w')
  for line in cont_lines:
    fp.write(line)
  fp.close()

if __name__ == '__main__':
  prefix = ('_'.join(sys.argv[1:]) + '_').upper()
  for root, dirs, files in os.walk('.'):
    for file_name in files:
      if not file_name.endswith(".h"):
        continue
      file_path = root + '/' + file_name
      guard = prefix + '_'.join([root, file_name])[2:].replace('.', '_').replace('/', '_').upper() + '_'
      UpdateGuard(file_path, guard)
