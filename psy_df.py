# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 16:43:35 2016

@author: advena
"""

#reference: http://pandas.pydata.org/pandas-docs/stable/10min.html 

def df_dupes(df_in):
    '''
    Returns [object,count] pairs for each unique item in the dataframe.    
    '''
    # import pandas
    if isinstance(df_in, list) or isinstance(df_in, tuple):
        import pandas as pd
        df_in = pd.DataFrame(df_in)
    return df_in.groupby(df_in.columns.tolist(),as_index=False).size()

def df_filter(df_in, sub_str, col_index=-1): # soln_text
    '''
    filter a python list using a regular expression
    
    parameters
        df_in: 2-dimensional list-like item  to be filtered.
        reges_str: regular expression (before compile)
    
    '''
    import pandas as pd
    #import re
    testing = True   # print extra data to the console for debugging
    if testing: 
        print('')        
        print('df_filter starting')   
        print('    sub_str: ' + sub_str)
        print('    df_in rows: ' + str(len(df_in)))
    lst=[]
    for index, row in enumerate(df_in.values):
        #pattern = re.compile(sub_str)
        if sub_str in (str(row[int(col_index)])):
            lst += [row]
    col_names = ['Interval','Iterations','Pms','Qms','P_Mismatch','P_Bus#','P_BusName','P_Volt','P_VoltMagPU',\
             'QmaxMism','Q_Bus#','Q_BusName','Q_Volt','Q_VoltMagPU','Solution Attempt']
    df_out = pd.DataFrame(lst, columns=col_names)

    if testing: print('df_filter finished.  return rows: '  + str(len(df_out)))   
    return df_out   
    
def df_compare(df1, df2, compare_col_list, join_type):
    '''
    df_compare compares 2 dataframes.
    Returns left, right, inner or outer join
    df1 is the first/left dataframe
    df2 is the second/right dataframe
    compare_col_list is a lsit of column names that must match between df1 and df2
    join_type = 'inner', 'left', 'right' or 'outer'
    '''              
    import pandas as pd
    return pd.merge(df1, df2, how=join_type,
                on=compare_col_list)

def df_compare_examples():
    import pandas as pd
    import numpy as np
    df1=pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns = ['c1', 'c2', 'c3'])
    '''        c1  c2  c3
            0   1   2   3
            1   4   5   6
            2   7   8   9   '''
    df2=pd.DataFrame([[4,5,6],[7,8,9],[10,11,12]], columns = ['c1', 'c2', 'c3'])
    '''        c1  c2  c3
            0   4   5   6
            1   7   8   9
            2  10  11  12   '''
    # One can see that df1 contains 1 row ([1,2,3]) not in df3 and 
    # df2 contains 1 rown([10,11,12])  not in df1.
    
    # Assume c1 is not relevant to the comparison.  So, we merge on cols 2 and 3.
    df_merge = pd.merge(df1,df2,how='outer',on=['c2','c3'])
    print(df_merge)
    '''        c1_x  c2  c3  c1_y
            0     1   2   3   NaN
            1     4   5   6     4
            2     7   8   9     7
            3   NaN  11  12    10   '''
    ''' One can see that columns c2 and c3 are returned.  We also received
            columns c1_x and c1_y, where c1_X is the value of column c1
            in the first dataframe and c1_y is the value of c1 in the second
            dataframe.  As such, 
               any row that contains c1_y = NaN is a row from df1 not in df2 &  
               any row that contains c1_x = NaN is a row from df2 not in df1. ''' 
    df1_unique = pd.merge(df1,df2,how='left',on=['c2','c3'])
    df1_unique = df1_unique[df1_unique['c1_y'].isnull()]
    print(df1_unique)
    df2_unique = pd.merge(df1,df2,how='right',on=['c2','c3'])
    print(df2_unique)
    df_common =  pd.merge(df1,df2,how='inner',on=['c2','c3'])
    print(df_common)


def delete_column_example():
    print 'create df'
    import pandas as pd
    df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns=['a','b','c'])
    print 'drop (delete/remove) column'
    col_name = 'b'
    df.drop(col_name, axis=1, inplace=True)  # or  df = df.drop('col_name, 1)
    
def delete_rows_example():
    print '\n\ncreate df'
    import pandas as pd
    df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns=['col_1','col_2','col_3'])
    print(df)
    print '\n\nappend rows'
    df= df.append(pd.DataFrame([[11,22,33]], columns=['col_1','col_2','col_3']))
    print(df)
    print '\n\ndelete rows where (based on) column value'
    df = df[df.col_1 == 4]
    print(df)