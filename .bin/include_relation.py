#!/usr/bin/env python

import os
import sys
import re

def GetFileNameIncluded(line):
    line = line.replace('<', '\"')
    line = line.replace('>', '\"')
    first_pos = line.find('\"')
    second_pos = line.find('\"', first_pos + 1)
    return line[first_pos + 1 : second_pos].split('/')[-1]

if __name__ == '__main__':
    fp = open("include.dot", "w")
    fp.write('digraph {\n')
    include_expr = re.compile('#include')
    for root, dirs, files in os.walk('.'):
        for file_name in files:
            if file_name.endswith('.cpp') \
                    or file_name.endswith('.cu') \
                    or file_name.endswith('.h') \
                    or file_name.endswith('.cuh') \
                    or file_name.endswith('.c') \
                    or file_name.endswith('.cc'):
              file_path = root + '/' + file_name
              for line in open(file_path, 'r'):
                  if '#include' in line:
                      included_file = GetFileNameIncluded(line)
                      fp.write('\"' + included_file + '\"->\"' + file_name + '\"\n')
    fp.write('}\n')
    fp.close()
    os.system("dot -Tpng -O include.dot && rm include.dot")
