# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:43:39 2016

@author: chris
"""

# --------------------------------------
#   psyops Fixed Width 
# --------------------------------------

'''    
moved to psyops filemngr.py
def filter_file_lines(file_in, regex_str):
    import pandas as pd
    import re
    lines = []  # pandas.DataFrame()
    pattern = re.compile(regex_str)
    for i, line in enumerate(open(file_in)):
        for match in re.finditer(pattern, line):
            lines+=[line]
    return lines   #df.to_list()  #pandas.DataFrame(lst)
def filter_file_lines_test():
    file_in = r'K:\AFC Model Solution Logs\log\log_hourly48.txt'
    regex_str = regex_str = '\d\d\ amb_solve\d\.dir' 
    print(filter_file_lines(file_in, regex_str))
'''

def find_col_specs(lines_list, max_nonspace = 0, return_widths = False):
    #import pandas as pd
    #from psyops import filemgnr as fm
    nonspace_cnt=[]
    for line_num in range(len(lines_list)):
        while len(nonspace_cnt) < len(lines_list[line_num]):
            nonspace_cnt += [0]
        #count non-space characters in each column.
        for char_pos in range(len(lines_list[line_num])):
            curr_line = lines_list[line_num]
            if curr_line[char_pos] != ' ':
                nonspace_cnt[char_pos] +=1
    col_start = [0]
    col_specs = []
    col_width = []
    for char_pos in range(1, len(nonspace_cnt)):
        if nonspace_cnt[char_pos] > max_nonspace \
           and nonspace_cnt[char_pos-1] <= max_nonspace:
              col_start += [char_pos] 
              col_specs += [[ col_start[-2], col_start[-1] ]]
              col_width += [int(col_start[-2]) - int(col_start[-1]) + 1]
    if col_start[-1] < len(nonspace_cnt):
        col_specs += [ [col_start[-1], len(nonspace_cnt)] ]
        col_width += [col_start[-2] - col_start[-1] + 1]
    
    if return_widths:
        return col_width
    else:
        return col_specs
def find_col_specs_test():
    from psyops import psy_file as fm    
    file_in = r'K:\AFC Model Solution Logs\log\log_yearly.txt'
    regex_str = '\d\d\ amb_solve\d\.dir' 
    lines_list = fm.filter_file_lines(file_in, regex_str)
    #lines_list = ["asdfafds asdfasdf sdfsdfgsdfgsdfg    sdfgsdfgsdf        dfg",
    #              "asdfasdf  asdfasd asdfasdfasdfa        asdfasdfas       df"]
    col_specs = find_col_specs(lines_list, max_nonspace = 0, return_widths = False)
    print col_specs
    
def parse_fw_lines(line_list, col_specs, strip_chars_list=', '):
    ret = []
    spre = '[ '
    s1 = 'line_list['
    s2 = str(0)  #str(line_num)
    s3 = ']['
    s4 = str(0)  #str(col_specs[j][0])
    s5 = ':'
    s6 = str(0)  #str(col_specs[j][1])
    s7 = ']'
    s8 = '.strip("' + strip_chars_list + '")'
    spost = ' ]'
    
    line_num = 0
    for i in range(len(line_list)):
        s = spre
        for j in range(len(col_specs)):
            s2 = str(line_num)
            try:
                s4 = str(col_specs[j][0])
                s6 = str(col_specs[j][1])
                if j > 0: s += ', '
                s += s1 + s2 + s3 + s4 + s5 + s6 + s7 +s8
            except:
                print('line ' + str(i) + ', char pos: ' + str(j))
                s4=''
                break
        s += spost
        #print s
        if len(s4)>0: ret += [eval(s)]
        line_num += 1
    return ret

def parse_fw_lines_test():
    line_list =['abc def    ghi   jk', \
                'lm  no     pqrst uvw']
    col_specs=[[0,4],[4,11],[11,17],[17,20]]
    ret = parse_fw_lines(line_list, col_specs=col_specs, strip_chars_list=' ')
    print ret
    
    
def test_all():
    print(' ')
    print(' ')
    find_col_specs_test()
    print(' ')
    print(' ')
    parse_fw_lines_test()

    
    
test_all()
# --------------------------------------
#   temp
# --------------------------------------



