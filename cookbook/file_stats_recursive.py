# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:57:18 2016

@author: advena
"""
#-------------------------------------------------------------------#
#   User Input                                                      #
search_path = r'K:/Afzal_1/ATCPJM_PRD1_201606161023'
file_pattern = '*.*'
recursive_search = True
relative_path = True  #  True: output will have relative path
#                       False: output will have absolute path
result_file = search_path + '/' + 'file_stats.csv'
open_excel = True
#   End of User Input                                               #
#-------------------------------------------------------------------#

import os
import pandas as pd
from fnmatch import filter

# import psyops as po
# from psyops import find_files

def find_files(search_path, pattern='**', recursive=False):
        if recursive:
            ret = []
            for base, dirs, files in os.walk(search_path):
                goodfiles = filter(files, pattern)
                ret.extend(os.path.join(base, f) for f in goodfiles) #.replace('\\','/')
            return ret
        else:
            return filter(os.listdir(search_path), pattern)

def excel_open(filename, vis=True):
    '''
    Open file in MS Excel application.
    Parameters:
        filename (str): name of file Excel will open
        vis (boolean):  see the spreadsheet?
    '''
    from win32com.client import Dispatch
    xl = Dispatch('Excel.Application')
    wb = xl.Workbooks.Open(filename)
    if vis:
        xl.Visible = True # optional

# recursive file search
file_names = find_files(search_path, file_pattern, recursive_search)

# create empty dataframe
col_names=['folder','file.ext','size (kB)','row count']
df = pd.DataFrame(columns=col_names)

# append file stats to df
for f in file_names:
    full_path = os.path.join(search_path,f).replace('\\','/')
    folder = str(os.path.split(full_path)[0])
    if relative_path:
        folder = folder[len(search_path)+1:]
    if len(folder)==0: folder=''
    file_name = os.path.split(full_path)[-1]
    file_size = os.stat(full_path).st_size
    file_rows = len(list(open(full_path)))+1
    print 'reading: ', file_name, 'from', folder
    df = df.append(pd.DataFrame([[folder, file_name, long(file_size)1000, file_rows]], columns=col_names))
# Sample results
print df.head(3)
print '...'
print df.tail(3)

# Save results and open in Excel
df.to_csv(result_file)
if open_excel: excel_open(result_file)