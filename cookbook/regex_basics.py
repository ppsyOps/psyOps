# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:33:52 2016

@author: advena
"""
import re

# search: string contains pattern
re_str = re.compile('I')   # string pattern
re_cmpl = re.compile(re_str)  # compiled pattern
look_in = 'string in which I am seeking'
if re.search(re_str, look_in):
    print('Found it.')
else:
    print('Did not find it.')

# search: string begins with pattern
if re.match(re_str, look_in):
    print('Found it.')
else:
    print('Did not find it.')
    
# loop with regex
re_str = 'a'
re_cmpl = re.compile(re_str)  # compiled pattern
look_in = 'Adam ate an apple'
i = 0
for search in re.finditer(re_cmpl, look_in):
    i += 1
print("Found " + str(i) + " lowercase a's.")