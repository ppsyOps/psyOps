# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 13:17:15 2016

@author: advena
"""


def soln_col_specs_old(line1_str):
    lst = [[0, 0], [0, 5], [5, 15], [15, 25], [25, 33], [33, 37], [37, 39], \
           [39, 51], [51, 61], [61, 71], [71, 79], [79, 84], [84, 97], \
           [97, 107], [107, 122], [122, 125]]
    i = len(line_list[0].split(' ')[0]) + 2  # get width of 1st item in col1 and add 2 (since hour goes from hour1 to hour186)
    #print(i)
    lst = [[item[0]+i,item[1]+i] for item in lst]
    lst[0][0] = 0
    return lst
def soln_col_specs_old_test():
    line_list = ['day1   asdfasd adsfasdf adfasdf']
    line1 = line_list[0]
    print soln_col_specs(line1)