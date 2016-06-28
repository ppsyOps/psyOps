# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:28:45 2016

@author: advena
"""

#create a dataframe
import pandas as pd
df = pd.DataFrame([[1,'John','Doe'],[2,'Jane','Doe'],[3,'Don','Juan de Marco']],columns=['id', 'fname', 'lname'])



def compare_frames_example():
    import pandas as pd
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
    print(df1_unique)
    df2_unique = pd.merge(df1,df2,how='right',on=['c2','c3'])
    print(df2_unique)
    df_common =  pd.merge(df1,df2,how='inner',on=['c2','c3'])
    print(df_common)