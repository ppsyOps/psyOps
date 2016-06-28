# -*- coding: utf-8 -*-
"""
Created on Wed Apr 5 2016
@author: advena

'''
List of functions:
    path_uniquifier() removes duplicates from sys.path without affecting orde
    path_append(file_name) loads finds file_name and appends file_names's path 
                           to sys.path if not already in there.  
                           file_name default: 'psy_readme.txt', which will
                           append psyops module to sys.path
    me_path(file_name) returns the path in which parameter file_name is found.
                       Specify a filename that can only be found in this python 
                       script's root folder
"""

# ----------------------------------------------------------------------------    
#  Function definitions
# ----------------------------------------------------------------------------    

def path_uniquifier():
    '''
    Remove duplicates from sys.path without affecting order
    '''
    from sys import path
    seen = set()
    seen_add = seen.add
    sys_path = [x for x in path if not (x in seen or seen_add(x))]
    path = sys_path

def path_append(file_name='psy_readme.txt'):
    '''
    path_append() loads finds file_name and appends 
    file_names's path to sys.path if not already in there.
    
    Depends on me_path().
    
    Consider following up with a run of path_uniquifier().
    '''
    import sys
    new_path = me_path(file_name)    
    try:
        sys.path.index(new_path)
        return 'already in path'
    except:
        try:
            sys.path.append(new_path)
            return sys.path
        except:
            print('Unable to to import required psyops library.  Script will fail.')
            return False



def me_path(file_name='psy_readme.txt'):
    '''
    me_path() returns the path in which parameter file_name is found.
    specify a filename that can only be found in his python script's
    root folder 
    '''
    import sys
    import os
    from fnmatch import filter    
    exec_pre = sys.exec_prefix
    for sf in [r'Lib\site-packages\psyops', 'Lib', '']:
        try:
            ret=[]
            for base, dirs, files in os.walk(os.path.join(exec_pre, sf)):
                goodfiles = filter(files, file_name)
                ret.extend(os.path.join(base, f) for f in goodfiles)
            return ret[0][:-15]
        except:
            'try again'

    
def sys_path_append(file_name='psy_readme.txt'):
    '''
    combines me_path, path_append and path_uniquifier in one function.
    '''

    import sys
    import os
    from fnmatch import filter  
    
    # set new_path = path in which parameter file_name is found.
    new_path = ''
    for sf in [r'Lib\site-packages\psyops', 'Lib', '']:
        try:
            ret=[]
            for base, dirs, files in os.walk(os.path.join(sys.exec_prefix, sf)):
                goodfiles = filter(files, file_name)
                ret.extend(os.path.join(base, f) for f in goodfiles)
            new_path =  ret[0][:-15]
        except:
            'try again'
    
    # load new_path into sys.path
    if new_path != '':
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
