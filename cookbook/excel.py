# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\advena\.spyder2\.temp.py
"""

def excel_open(filename, vis=True):
    '''
    Open MS Excel.  Have Excel open file: filename
    Parameters:
        filename (str): name of file Excel will open
        vis (boolean):  see the spreadsheet?
    '''
    from win32com.client import Dispatch
    xl = Dispatch('Excel.Application')
    wb = xl.Workbooks.Open(filename)
    if vis:
        xl.Visible = True # optional
