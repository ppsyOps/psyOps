# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:58:19 2016

@author: advena
"""

###################################
########     example 1     ########
###################################
print('')
print(' ***** example 1 ***** ')
print('')
import pandas as pd

gen_dtype={'Bus_Num':'int', 'ID':'str', 'Pgen':'float', 'Qgen':'float', \
          'Qmax':'float', 'Qmin':'float', 'VSched_pu':'float',\
          'Remote_Bus_Num':'int','Mbase':'float', \
          'R_source_pu':'float', 'X_source_pu':'float',\
          'RTran_pu':'float', 'XTran_pu':'float','Gentap_pu':'float', \
          'In_Service':'int', 'RMPCT':'float','Pmax':'float',\
          'Pmin':'float','Owner':'int','Owner_Fraction':'float'}

gen_cols=['Bus_Num', 'ID', 'Pgen', 'Qgen', \
          'Qmax', 'Qmin', 'VSched_pu',\
          'Remote_Bus_Num','Mbase', \
          'R_source_pu', 'X_source_pu',\
          'RTran_pu', 'XTran_pu','Gentap_pu', \
          'In_Service', 'RMPCT','Pmax',\
          'Pmin','Owner','Owner_Fraction']

gen_df=pd.DataFrame(columns=gen_cols)

for key in gen_dtype:
    code_str="gen_df['" + key + "']=gen_df['" + key + \
             "'].astype(gen_dtype['" + key + "'])"
    exec code_str

print gen_df.dtypes


###################################
########     example 2     ########
###################################

print('')
print('')
print(' ***** example 2 ***** ')
print('')

import sys
import StringIO

# create file-like string to capture output
codeOut = StringIO.StringIO()
codeErr = StringIO.StringIO()

code = """
def f(x):
    x = x + 1
    return x

"""

# capture output and errors
sys.stdout = codeOut
sys.stderr = codeErr

exec code

# restore stdout and stderr
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

print f(4)

s = codeErr.getvalue()
print('\n')
if not s=='':
    print 'This is my output.'
    print "error:%s\n" % s
    s = codeOut.getvalue()
    print "output:\n%s" % s

codeOut.close()
codeErr.close()
