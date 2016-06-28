# -*- coding: utf-8 -*-
"""
Name: generateHTMLFolderList.py
Description: generates an HTML file that lists the files in a path. The hyperlinks to the files open the files in the web browser
Input: Please see user input section
Output: Please look for outputFile.html in the root_path
"""
#----------------------------------------------#
# User Input  
root_path=r'K:\AungThinzar\Cont'
pattern='*.*'
#----------------------------------------------#

import os

# Get the full_path and recessive search of files
dir_list = []
for base, dirs, files in os.walk(root_path):
    goodfiles = filter(files, pattern)
    dir_list.extend(os.path.join(base, f) for f in goodfiles)

# Extract the filenames using list comprehension
filenames = [os.path.basename(full_path) for full_path in dir_list]

'''#old way of extracting filenames
filenames = []
for full_path in dir_list:
    filenames.append(os.path.basename(full_path))
'''

# Write the file list to the html file
with open(root_path + '/outputFile.html', 'w') as f:
    for idx, filename in enumerate(filenames): 
        f.write("<a href=\""+dir_list[idx]+"\">"+filename+"</a><br/>\n")
