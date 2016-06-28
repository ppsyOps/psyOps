# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''


'''
import os
from fnmatch import filter
import re
import time
from datetime import datetime as dt

def modified_time(file_name):
    if os.path.exists(file_name):
        return time.ctime(os.path.getmtime(file_name))
    else:
        return
    
def created_time(file_name):
    if os.path.exists(file_name):
        return time.ctime(os.path.getctime(file_name))
    else:
        return

def touch(file_name):
    # Update the modified timestamp of a file to now.
    if not os.path.exists(file_name):
        return
    try:
        os.utime(file_name, None)
    except Exception:
        open(file_name, 'a').close()

def midas_touch(root_path, older_than=dt.now(), pattern='**', recursive=False):
    '''
    midas_touch updates the modified timestamp of a file or files in a 
                directory (folder)
    
    Arguements:
        root_path (str): file name or folder name of file-like object to touch
        older_than (datetime): only touch files with datetime older than this 
                   datetime
        pattern (str): filter files with this pattern (ignored if root_path is
                a single file)
        recursive (boolean): search sub-diretories (ignored if root_path is a 
                  single file)
    '''
    # if root_path NOT exist, exit
    if not os.path.exists(root_path):
        return
    # if root_path DOES exist, continue.
    else:
        # if root_path is a directory, touch all files in root_path
        if os.path.isdir(root_path):
            # get a directory list (list of files in directory)
            dir_list=find_files(root_path, pattern='**', recursive=False)
            # loop through list of files
            for f in dir_list:
                # if the file modified date is older thatn older_than, touch the file
                if dt.fromtimestamp(os.path.getmtime(f)) < older_than:
                    touch(f)
                    print "Touched ", f
        # if root_path is a file, touch the file
        else:
            # if the file modified date is older thatn older_than, touch the file
            if dt.fromtimestamp(os.path.getmtime(f)) < older_than:
                touch(root_path)

def directory(folder):
    '''
    This def is just and exmaple.
    return directory listing of 'folder'
    '''
    return os.listdir(folder)

def file_empty(fname):
    try:
        return os.stat(fname).st_size == 0
    except:
        return True
        
def txt_file_empty(fname):
    try:
        with open(fname) as f:
            for l in f:
                return False
    except IOError:
        return True    
    return True

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
def filter_file_lines(file_in, regex_str):
    #import pandas as pd
    lines = []  # pandas.DataFrame()
    print ("regex: ", regex_str)
    pattern = re.compile(regex_str)
    
    for line in open(file_in):
        for match in re.finditer(pattern, line):
            lines+=[line]
    
    return lines   #df.to_list()  #pandas.DataFrame(lst)    
    
def filter_file_lines_test():
    file_in = r'K:\AFC Model Solution Logs\log\log_hourly48.txt'
    regex_str = '\d\d\ amb_solve\d\.dir' 
    print(filter_file_lines(file_in, regex_str))

def find_files(root_path, pattern='**', recursive=False):
    try:
        if recursive:
            ret = []
            for base, dirs, files in os.walk(root_path):
                goodfiles = filter(files, pattern)
                ret.extend(os.path.join(base, f) for f in goodfiles)
            return ret
        else:
            return filter(os.listdir(root_path), pattern)
    except:
        print 'Error: find_files(' + str(root_path) + ', ' + str(pattern) + ') failed.'
        return []  #return empty array to assure calling code does not fail

def find_files_test():
    print('Non-recurive: c:\temp')
    ret = find_files(r'C:\temp', '*.*', False)
    print(ret)
    print('')
    print 'Recurive: c:\temp'
    ret = find_files(r'C:\temp', '*.*', True)
    print(ret)

def test_all():
    filter_file_lines_test()
    print('')
    print('')
    find_files_test()