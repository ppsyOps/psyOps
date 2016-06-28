# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 14:38:55 2016

@author: advena
"""

def psy_path(file_name='psy_readme.txt'):
    import sys
    import os
    from fnmatch import filter    
    exec_pre = sys.exec_prefix
    for sf in [r'Lib\site-packages\psyops', 'Lib', '']:
        try:
            ret=[]
            if sf != '':
                for base, dirs, files in os.walk(os.path.join(exec_pre, sf)):
                    goodfiles = filter(files, file_name)
                    ret.extend(os.path.join(base, f) for f in goodfiles)
                return ret[0][:-15]
            else:
                for base, dirs, files in os.walk(exec_pre):
                    goodfiles = filter(files, file_name)
                    ret.extend(os.path.join(base, f) for f in goodfiles)
                return ret[0][:-15]
        except:
            'try again'

def psy_path_append(file_name='psy_readme.txt'):
    '''
    sys_path_append() loads this python scripts path into sys.path 
    '''
    from sys import path
    new_path = me_path(file_name)    
    try:
        sys.path.index(new_path)
    except:
        try:
            sys.path.append(new_path)
        except:
            print('Unable to to import required psyops library.  Script will fail.')
            return False
    # remove duplicates from sys.path 
    seen = set()
    seen_add = seen.add
    sys_path = [x for x in sys.path if not (x in seen or seen_add(x))]
    sys.path = sys_path
    return True
# -------------------------------------------------------------------
# allow execution as command line script: python soln3_fixer.py
# -------------------------------------------------------------------
if __name__ == "__main__":
    psy_path_append()
    #import psyops