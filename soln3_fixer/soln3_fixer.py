# -*- coding: utf-8 -*-
'''
Check production for solution 3. 
If found, report the max p and q mismatch busses
and their areas.
'''
import pandas as pd
import datetime
from datetime import timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import os
from os import path
from os.path import join
import re
import shutil
# psyops is Advena's python library for lazy power systems engineers
from psyops import psy_types
from psyops.psy_types import is_str
from psyops.psy_types import to_datetime
from psyops.psy_types import type_fixer
from psyops import psy_file as pf  
from psyops.psy_file import file_empty
from psyops.psy_str import space_split
from psyops.soln3_fixer import soln3_config as cfg
global cfg
global non_converge


def min_list_2d(list_in, compare_col, ret_col):
    return min((e for e in list_in if e[compare_col]), \
               key = itemgetter(1))[ret_col]

def max_list_2d(list_in, compare_col, ret_col):
    return max((e for e in list_in if e[compare_col]), \
               key = itemgetter(1))[ret_col]

def extract_posint(str_in):
    ret = ''
    str_in = str(str_in).strip()
    for chr in str_in:
        if chr.isdigit():
           ret += chr
    return int(chr)

# -------------------------------------------------------------------
#              soln 3 fixer specific functions
# -------------------------------------------------------------------
def extract_increment(line):
    ret = ''
    for chr in line:
        if not chr.isdigit():
            ret += chr
        else:
            break
    return ret

def snap_dt_adder(first_snap_dt, snap_num, incr):

    first_snap_dt = psy_types.to_datetime(first_snap_dt,[])
    incrs=int(snap_num)-1
    td_dict = {'h':timedelta(hours=incrs),  \
               'd':timedelta(days=incrs), \
               'w':timedelta(weeks=incrs), \
               'm':relativedelta(months=incrs), \
               'y':relativedelta(years=incrs) }
    return td_dict[(incr.lower())[0]]


def pathfile_out():
    if '\\' in cfg.file_out or '/' in cfg.file_out:
        return cfg.file_out
    elif len(cfg.file_out) > 1:
        return join(cfg.dir_out, cfg.file_out)
    else:
        return

def soln_summary_regex(regex_str='auto', compiled=False):
    if regex_str == 'auto' or len(regex_str) == 0:
        if cfg.soln_num == 0:
            regex_str = r'\d\d\ amb_solve\d\.dir'
        else:
            regex_str = r'\d\d\ amb_solve' + cfg.soln_num + '.dir'
    if compiled:    
        return re.compile(regex_str)
    else:
        return regex_str

def created_regex(regex_str='auto'):
    if regex_str == 'auto' or len(regex_str) == 0:
        if cfg.soln_num == 0:
            regex_str = cfg.regex_created_pattern
    return re.compile(regex_str)

def file_name_fixer(file_name, date_suffix=None):

    # break Humpty into pieces, split at each period (.)
    temp = file_name.split('.')  
    if len(temp) == 1: temp += [cfg.ext.strip('. ')]

    # Let's get the processing of the date_suffix out of the way
    if date_suffix == None:
        date_suffix = ''
    elif is_str(date_suffix):
        date_suffix = date_suffix.strip().replace('/','-')
        date_suffix = date_suffix.replace(' ','_').replace(':','')
    elif isinstance(date_suffix, datetime.datetime):
        s =  "_" + str(date_suffix)[:16]  # convert date to string to the minute
        date_suffix = s.replace(' ','_').replace(':','') # convert to clean file name
    elif isinstance(date_suffix, bool):
        if date_suffix:
            date_suffix = datetime.datetime.now()[:16]
    else:
            date_suffix = ''
    if len(date_suffix) > 0:
        if not date_suffix[0] in ['_','-']:
            date_suffix = '_' + date_suffix
            
    # Add the date_suffix to the end of the filename and before the extension.
    if len(temp) > 1:
        # there is an extension, so add date suffix to next to last list item
        temp[-2] = temp[-2] + date_suffix
    else:
        # only get here is cfg.ext is not set properly in the config file 
        temp[-1] = temp[-1] + ['csv']
        
    # put Humpty (the filename) back together again        
    file_name = '.'.join(temp)

    # If the provided fileneame includes / or \, it is a complete path.
    # otherwise, insert cfg.dir_out (from config file) at the beginning.
    if not ('/' in file_name or '\\' in file_name):
        file_name = path.join(cfg.dir_out, file_name)

    return file_name


def parse_snapshot_def(log_file, line_num, increment, line):
    '''
    snapshot_def_cols = ['log_file', 'Log_date', 'log_line', \
                     'Increment', 'snapshot_num', \
                     'snapshot_datetime', 'snapshot_hour']
    '''
    # " ------------------ Creating snapshot 25 for  2016-05-03 00:00 ---------------"
    # word:    0              1        2     3   4     5          6        7
    temp = space_split(line)
    # snapshot_def_cols taken from config file:            
    # ['log_line', 'snapshot num', 'snapshot datetime', 'hour', 'log datetime']
    try:            
        snap_num = int(temp[3])
    except:    
        snap_num = str(temp[3])
    dt = temp[5] + ' ' + temp[6]
    try:
        dt = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M')
    except:
        dt = dt  
    try:
        hr = int(temp[6][:2])
    except:
        hr = temp[6][:2]  

    return [log_file, None, line_num, increment, snap_num, dt, hr]

def get_soln3_meta(soln_summary):
    '''
    Metadata about solution 3 snapshots from the soln_summary table.  
    Returns list: [soln3_summary, before_snap3, first_snap3, last_snap3, \
                 after_snap3, snap3_cnt, snap_cnt]
        soln3_summary = soln_summary list filtered to only soln3 snapshots        
        before_snap3 = number of last snap_shot before first soln3
        before_snap3 = number of last snap_shot before soln3
        before_snap3 = number of last snap_shot before soln3
        after_snap3 = number of first snap_shot after last soln3
        snap3_cnt: count of solution 3 snapshots
        snap_cnt: count of all solutions (number of snapshots, converged or not)
    '''
    try:
        soln3_snaps = [ item for item in soln_summary if item[-1] == 3 ]
    except:
        return []
    if len(soln3_snaps) == 0:
        #return [None, None, None, None, None, None, None]
        return []
    else:
        snap_cnt = len(soln_summary)
        snap3_cnt = len(soln3_snaps)
        #           min_list_2d(list2D, compare_col, ret_col)
        first_snap = min_list_2d(soln_summary, 4, 4)
        last_snap = max_list_2d(soln_summary, 4, 4)
        first_snap3 = min_list_2d(soln3_snaps, 4, 4)
        last_snap3 = max_list_2d(soln3_snaps, 4, 4)
        # find snapshot before first soln 3        
        if first_snap3 > first_snap:
            before_snap3 = first_snap3 - 1
        else:
            before_snap3 = None
        # find snapshot after last soln 3        
        if last_snap3 < last_snap:
            after_snap3 = last_snap3 - 1
        else:
            after_snap3 = None

        return [soln3_snaps, before_snap3, first_snap3, last_snap3, \
                 after_snap3, snap3_cnt, snap_cnt]
 

def parse_non_converge_pt1(log_file, line_num, increment, snap_num, line):
    # sample line from logfile:            
    # " day25. Fast Dec LF didn't converge in 60 iteration"
    #     0      2   2   3   4       5      6  7     8
    '''
    non_converge_cols = ['log_file', 'Log_date', 'log_line', \
                     'Increment', 'snapshot_num', 'num_iterations', \
                     'tot_mismatch', 'mismatch_bus_count', 'tolerance'] 
    '''
    temp = space_split(line)
    non_cvg_line_num = line_num
    return [log_file, None, non_cvg_line_num, \
            increment, snap_num, temp[7], \
             None, None, None]
    
def parse_non_converge_pt2(line_num, line, non_converge_row):

    ret = non_converge_row
    non_cvg_line_num = ret[2]
    if non_cvg_line_num == line_num:
        'skip line'
    else:  # read 24 lines after non-convergence is reported
        '''
        non_converge_cols = ['log_file', 'Log_date', 'log_line', \
                         'Increment', 'snapshot_num', \
                         'num_iterations', 'tot_mismatch', \
                         'mismatch_bus_count', 'tolerance']    temp = space_split(line)
        '''
        if len(line.strip()) == 0:
            'skip blank line'
        elif 'totalAlgebMism' in line:  #find total mismatch
            # sample line from logfile:            
            #    " totalAlgebMism=141519.060"
            #  word:     0           1
            temp = line.split('=')  #split line on "=" sign.
            temp = [item.strip() for item in temp] # clean lead/lag spaces
            try:
                ret[6] = float(temp[1]) #total mismatch
            except:
                ret[6] = temp[1] #total mismatch
        elif 'buses with mismatch > tolerance' in line:
            # sample line from logfile:            
            #    " Total 7712 buses with mismatch > tolerance=   5.00000 "
            #  word: 0    1     2     3     4     5     6           7
            temp = space_split(line)
            try:
                ret[7] = int(temp[1]) # mismatch bus count
                ret[8] = int(temp[-1]) # tolerance
            except:
                ret[7] = temp[1] # mismatch bus count
                ret[8] = temp[-1] # tolerance
            if cfg.verbose:
                print('non_converge[-1]: '+ str(cfg.non_converge_cols)) 
                print(ret[-1])
            ret[4] = temp[1] #total mismatch          
    # return values    
    return ret
    
def parse_bus_mismatch(file_in, line_num, line, increment, snap_num):
    '''
    bus_mismatch_cols = ['log_file', 'Log_date', 'log_line', \
                         'Increment', 'snapshot_num', \
                         'ibus', 'Bus_Num', 'Bus_Name', 'Volt', \
                         'Area_Num', 'Zone_Num', 'Mismatch_Magnitude', \
                         'P_Mismatch', 'Q_Mismatch', 'V_Magnitude', \
                         'V_Angle', 'V_Low', 'V_OK', 'V_High']
    '''
    try:  # only add lines where the first value is an integer
        temp = int((line[0:6].strip())) #if not an integer, skip
        return [file_in, None, line_num, \
               increment, snap_num, 
               line[0:6].strip(),line[7:13].strip(), line[14:26].strip(), line[27:31].strip(), \
               line[32:36].strip(), line[37:41].strip(), line[43:55].strip(), \
               line[56:68].strip(), line[69:81].strip(), line[82:92].strip(), \
               line[93:103].strip(), line[104:107].strip(), line[108::111].strip() ,line[112:115].strip()]
    except:
        return []
    
def parse_bus_mism_dtl(file_in, line_num, line, increment, snap_num):
    '''
     ******************* Detailed bus flow analysis for 314755 3SPOTSYL      115  345 DOM          1719 DVP          : *************
    word:     0             1      2   3      4      5     6     7            8    9   10           11   12          13 14                     
    bus_mism_dtl_cols = 
              ['log_file', 'Log_date', 'log_line', \
               'Increment', 'snapshot_num', \
               'Bus_Num', 'Bus_Name', 'Volt', \
               'Area', 'Zone', 'CKT', 'St', 'MW', 'MVAR', 'MVA', \
               'V_mag_[PU]', 'V_mag_[kV]', 'V_angle', 'Bus_Type', \
               'V_Type', 'Type', 'Tap_R', 'PS_Angle', 'TAP_R_To', \
               'branch_R', 'branch_X', 'branch_Chr', 'Rate_A', 'Rate_B', \
               'Rate_C', 'Metered', 'Length', 'Reg_Min', 'Reg_Max', \
               'Target_Min', 'Target_Max', 'MW_metered  MVAR_metered', \
               'MVA_metered', 'MW_loss', 'MVAR_loss']
    '''            
    try:
        bus_num = int(line[0:6].strip())
        bus_name = line[7:19].strip()
    except:
        bus_num = None
        bus_name = line[7:19].strip()
    try:  # only add lines where the first value is an integer
        ret = [[file_in, None, line_num, \
                increment, snap_num, \
                bus_num, bus_name, line[20:24].strip(), \
                line[25:29].strip(),line[30:34].strip(),line[35:39].strip(),\
                line[40:42].strip(),line[43:53].strip(),line[54:64].strip(),\
                line[65:75].strip(),line[76:86].strip(),line[87:97].strip(),\
                line[98:106].strip(),line[106:111].strip(),line[112:117].strip(),\
                line[117:123].strip(),line[124:131].strip(),line[132:139].strip(),\
                line[140:148].strip(),line[149:160].strip(),line[161:172].strip(),\
                line[173:184].strip(),line[185:192].strip(),line[193:200].strip(),\
                line[201:208].strip(),line[208:213].strip(),line[214:221].strip(),\
                line[222:232].strip(),line[233:239].strip(),line[240:248].strip(),\
                line[249:257].strip(),line[258:269].strip(),line[270:279].strip(),\
                line[280:290].strip(),line[291:301].strip(),line[302:312].strip()]]
    except:
        try:  # only add lines where the first value is an integer
            ret = [[file_in, bus_name, line_num, \
                    increment, snap_num, \
                    bus_num, bus_name, None, \
                    None, None, None,None, None, None, \
                    None, None, None, None, None, None, None, None, None, \
                    None, None, None, None, None, None, None, None, None, \
                    None, None, None, None, None, None, None, None, None]]
        except:
            'Skip line, it does not conform to a row in the bus mismatch details table '
            ret = []
    return ret

def parse_log_date(line, log_dt):
   
    # sample line: "   Created - Fri Apr 08 08:21:59 2016. TARA Ver 8.20 32-bit. LFCase-day35. . Rev-PTI32"            
    log_dt_line = True  # did we find the line containing the log date?
    for substr in cfg.log_date_substrs:
        if substr not in line:
            log_dt_line = False
    
    if log_dt_line:    
        log_dt = line[12:39].strip('. ')
        try:
            log_dt = datetime.strptime(log_dt,"%a %b %d %H:%M:%S %Y")
        except:
            try:
                log_dt = parse(log_dt)
            except:
                'leave log_dt in string format'
    return log_dt

def parse_gen_hdr_fr_to(line):
    temp = line.split('period')[-1].split('(')[0].strip()
    temp = temp.split(' to ')
    temp = [to_datetime(s.strip()) for s in temp]
    temp[-1] += timedelta(hours=1)
    return temp
    
def parse_gen_status_changes(log_file, line_num, line, increment, snap_num, \
                            gen_hdr_fr_to):  
    # test if  this line contains data.  If not bounce out  
    try:
        bus_num = int(line[:6].strip())
    except:
        #return [None]*len(cfg.gen_status_change_cols)
        return [] 
    # parse and return the current record
    return [log_file, None, line_num, \
            snap_num, gen_hdr_fr_to[0], gen_hdr_fr_to[1], \
            line[0:7].strip(), line[7:19].strip(), line[19:25].strip(), \
            line[25:29].strip(), line[29:35].strip(), line[35:39].strip(), line[40:49].strip(), \
            line[50:62].strip(), line[62:72].strip(), line[72:82].strip(), line[82:91].strip(), \
            line[91:101].strip(), line[101:120].strip(), line[120:].strip()]    
    '''  gen_status_change_cols = 
            ['log_file', 'Log_date', 'log_line', \
             snap_num, 'report_from', 'report_from', \
             'bus_num', 'bus_name', 'V', \
             'area', 'zone', 'ID', 'basCasMW', \
             'BasCsSta', 'PMin', 'PMax', 'Type', \
             'newSetPn', 'from_dt', 'to_dt']  '''    


def parse_branch_hdr_fr_to(line):
    return parse_gen_hdr_fr_to(line)

def parse_branch_status_changes(log_file, line_num, line, increment, snap_num, \
                            branch_hdr_fr_to):  
    # test if  this line contains data.  If not bounce out  
    try:
        bus_num = int(line[:6].strip())
    except:
        #return [None]*len(cfg.branch_status_change_cols)
        return [] 
    # parse and return the current record
    return [log_file, None, line_num, \
            snap_num, branch_hdr_fr_to[0], branch_hdr_fr_to[1], \
            line[0:7].strip(), line[7:19].strip(), line[19:25].strip(), line[25:30].strip(), line[30:35].strip(), \
            line[35:41].strip(), line[42:54].strip(), line[54:60].strip(), line[60:65].strip(), line[65:70].strip(), \
            line[72:74].strip(), line[75:78].strip(), line[78:87].strip(), line[87:96].strip(), line[96:105].strip(), \
            line[106:113].strip(), line[115:120].strip(), \
            line[120:129].strip(), line[129:138].strip(), line[138:148].strip(), \
            line[150:168].strip(), line[168:].strip()]
    '''  branch_status_change_cols = 
            ['log_file', 'Log_date', 'log_line', \
             'snap_num', 'report_from', 'report_from', \
             'bus_num_fr', 'bus_name_fr', 'v_fr', 'area_fr', 'zone_fr', \
             'bus_num_to', 'bus_name_to', 'v_to', 'area_to', 'zone_to', \
             'ckt', 'market', 'rate_a', 'rate_b', 'rate_c', \
             'status_type', 'base_case_st', \
             'new_rate_a', 'new_rate_b', 'new_rate_c', \
             'from_dt', 'to_dt' ]  '''    



def parse_xfmr_hdr_fr_to(line):
    return parse_gen_hdr_fr_to(line)

def parse_xfmr_status_changes(log_file, line_num, line, increment, snap_num, \
                            xfmr_hdr_fr_to):  
    # test if  this line contains data.  If not bounce out  
    try:
        #print(line[16:22].strip())
        #bus_num = line[16:22].strip()
        #print('bus_num: ' + bus_num)
        bus_num = int(bus_num)
    except:
        #return [None]*len(cfg.xfmr_status_change_cols)
        return [] 
    # parse and return the current record
    #print('line[0:15].strip() = ' + line[0:15].strip())
    return [log_file, None, line_num, \
            snap_num, xfmr_hdr_fr_to[0], xfmr_hdr_fr_to[1], \
            line[0:15].strip(' '), \
            line[15:22].strip(), line[22:36].strip(), line[36:40].strip(), \
            line[40:47].strip(), line[47:61].strip(), line[61:65].strip(), \
            line[65:72].strip(), line[72:85].strip(), line[85:90].strip(), \
            line[90:97].strip(), line[97:111].strip(), line[111:116].strip(), line[116:119].strip(), \
            line[119:128].strip(), line[128:137].strip(), \
            line[137:155].strip(), line[155:].strip()]   # 'from_dt', 'to_dt'
    '''  xfmr_status_change_cols = 
            ['log_file', 'Log_date', 'log_line', \
             'snap_num', 'report_from', 'report_from', \
             'trnsfrmr_name', \
             'w1_bus_num', 'w1_bus_name', 'w1_v', \
             'w2_bus_num', 'w2_bus_name', 'w2_v', \
             'w3_bus_num', 'w3_bus_name', 'w3_v', \
             'ntrl_bus_num', 'star', 'nmvl', 'ckt', \
             'status_type', 'action', \
             'from_dt', 'to_dt' ] '''    

def parse_soln_summary(log_file, log_dt, line_num, line, first_snap_dt):
    '''
    Sample from log_file:
    day_Ind #Itr #Pms #Qms  PmaxMism    Bus# BusName      Volt VoltMagPU  QmaxMism    Bus# BusName      Volt VoltMagPU ScriptFile 
    day1   40    0   24      0.01  997747 CRAWFORD T1  34.5    1.0322      0.00  997747 CRAWFORD T1  34.5    1.0322 amb_solve1.dir 

    soln_summary_cols = 
            ['log_file', 'Log_date', 'log_line', \
             'increment', 'snapshot_num', 'snap_date', 'snap_hr', \
             'iterations', 'Pms', 'Qms', 'P_Mismatch', 'P_Bus_Num', \
             'P_Bus_Name', 'P_Volt', 'P_Volt_Mag_PU', 'Qmax_Mismatch','Q_Bus#', \
             'Q_Bus_Name', 'Q_Volt', 'Q_Volt_Mag_PU', 'Solution_Attempt']
    '''
    ret = []
    soln_summary_pattern = soln_summary_regex('auto', compiled=False)
    #for match in finditer(soln_summary_pattern, line):
    if re.search(soln_summary_pattern,line):

        incr = line.lstrip()[0]  # first non-space character in the line
        increment = cfg.incr_dict[incr]
        snap_num = line[0:7].strip().split(' ')[0] # chars from first word in line
        snap_num = extract_posint(line[0:7].strip().split(' ')[0])
        if not isinstance(first_snap_dt, datetime.datetime):        
            first_snap_dt = parse(first_snap_dt) 
        snap_date = first_snap_dt + \
                snap_dt_adder(first_snap_dt, snap_num, incr)
        snap_hr = snap_date.hour
        iterations = line[-121:-116].strip()
        Pms = line[-116:-112].strip() 
        Qms = line[-111:-105].strip() 
        P_Mismatch = line[-104:-97].strip() 
        P_Bus_Num = line[-97:-90].strip()
        P_Bus_Name = line[-89:-77].strip() 
        P_Volt = line[-77:-71].strip() 
        P_Volt_Mag_PU = line[-70:-61].strip() 
        Qmax_Mismatch = line[-59:-51].strip() 
        Q_Bus_Num = line[-51:-43].strip() 
        Q_Bus_Name = line[-43:-31].strip() 
        Q_Volt = line[-31:-25].strip() 
        Q_Volt_Mag_PU = line[-23:-15].strip() 
        Solution_Attempt = line[-6:-4] 
        Solution_Attempt = [int(s) for s in Solution_Attempt if s.isdigit()]
        
        ret = [log_file, log_dt, line_num,\
                 increment, snap_num, snap_date, snap_hr, \
                 iterations, Pms, Qms, P_Mismatch, P_Bus_Num, \
                 P_Bus_Name, P_Volt, P_Volt_Mag_PU, Qmax_Mismatch,Q_Bus_Num, \
                 Q_Bus_Name, Q_Volt, Q_Volt_Mag_PU, Solution_Attempt]
    #  End of for loop        
        
    # if no match in this line, return empty list
    return ret

def report_from_log_file(file_in, type_conv=False, return_type=3):
    '''
    Fetch only the solution summary report from the bottom of the log file and
    parse the fixed width fields into a dataframe.  Return the dataframe.
    
    Parameters:
        file_in: the log file to read.  Must be a plain text file.
        type_conv: attempt to convert values to python data types.
        return_type:
            cfg.ret_bool   = 1 = output to file, return True/False
            cfg.ret_df     = 2 = return log info as list of dataframes
            cfg.ret_both   = 3 = output to file and return log info as list of dataframes
            cfg.ret_sqlite = 4 = output to sqlite database file

    '''
    # Initialize before looping through file lines  

    if cfg.verbose: 
        script_start = datetime.datetime.now()
        print('')
        print('------------------------------------------------------------')
        print('|--- Starting report_from_log_file: ' + file_in + ' ---|')
        print('------------------------------------------------------------')
        print('')
        print('---- parsing log_file: file: ' + file_in + '----')
        parse_start = datetime.datetime.now()

    # Initialize before looping through file lines  
    snap_num, soln_worst = 0, 0    
    snapshot_def, non_converge , bus_mismatch = [], [], []
    snapshot_def_substr = r"------------------ Creating snapshot"
    non_converge_substr = "Fast Dec LF didn't converge"
    bus_mism_dtl_substr = r"******************* Detailed bus flow analysis for"
    bus_mism_dtl, soln_summary, soln3_meta = [], [], []
    run_summary =  [None]*len(cfg.run_summary_cols)
    incr = file_in.split("_")[-1][0].strip() #h, d, w, m or y
    if file_in[-6:-4] == '48': 
        incr = 'H' #hourly 48
    increment = cfg.incr_dict[incr]
    non_cvg_line_num, bus_mism_dtl_line_num = -100, -100
    first_snap_dt, log_dt = None, None
    complete_log, in_gen_status_changes = False, False
    in_branch_status_changes, in_xfmr_status_changes = False, False
    gen_status_changes, branch_status_changes, xfmr_status_changes = [], [], []
    soln_summary_pattern = soln_summary_regex('auto', compiled=False)
    # ----------------------------------------------------------------
    # -----------      Start of file parsing Loop     ------------------
    # ----------------------------------------------------------------
    for line_num, line in enumerate(open(file_in)):     
        # snapshot definition       
        if snapshot_def_substr in line:
            #initialize for new snapshot
            snap_num = 0 
            non_cvg_line_num = -100
            bus_mism_dtl_line_num = -100
            snapshot_def += [parse_snapshot_def(file_in, line_num, increment, line)]
            snap_num = snapshot_def[-1][4]
            if first_snap_dt == None:
                first_snap_dt = snapshot_def[0][5]
        # reports of non-convergence
        elif non_converge_substr in line and not ('WarnID' in line):
            non_converge += [parse_non_converge_pt1(file_in, line_num, \
                                                    increment, snap_num, line)]
            non_cvg_line_num = line_num           
        # non convergence summary
        if non_cvg_line_num != -100  and \
           non_cvg_line_num < line_num and line_num <= non_cvg_line_num + 3:
               if non_converge[-1][2] == line_num:
                    non_converge[-1] = parse_non_converge_pt2(line_num, line, \
                                                              non_converge)
                    non_cvg_line_num = non_converge[-1][2]      
               else:
                    print('Error in report_from_log_file(). ' + \
                          'Unable to update non_converge report: ' + \
                          'non_converge[-1][2] != line_num. ')
       # bus mismatch summary
        if non_cvg_line_num != -100  and \
           non_cvg_line_num + 4 <= line_num and \
           line_num <= non_cvg_line_num + 25:
            if '*************' in line:
                non_cvg_line_num = -100
            else:            
                temp = parse_bus_mismatch(file_in, line_num, line, \
                                          increment, snap_num)
                if len(temp) > 1:
                    bus_mismatch += [temp]
                    if cfg.verbose:
                        #print('temp:')
                        #print(temp)
                        print('bus_mismatch: ' + str(cfg.bus_mismatch_cols))
                        print(bus_mismatch[-1])
        elif line_num > non_cvg_line_num + 25:
            non_cvg_line_num = -100
        # non convergence bus mismatch details
        if bus_mism_dtl_substr in line:
            bus_mism_dtl_line_num = line_num
        elif bus_mism_dtl_line_num + 1 < line_num and \
        line_num <= bus_mism_dtl_line_num + 6:  
            temp = parse_bus_mism_dtl(file_in, line_num, \
                                      line, snap_num, increment)
            if len(temp) > 1:
                bus_mism_dtl += temp
        elif line_num > bus_mism_dtl_line_num + 6:
            bus_mism_dtl_line_num = -100    

        # Gen Status Changes
        # Sample start/stop lines
        # ========= Report on generator status/dispatch changes for the period
        # ========= Total  772 Generators changed status    
        if "Report on generator status" in line:
            in_gen_status_changes = True
            gen_hdr_fr_to = parse_gen_hdr_fr_to(line)
        elif "Generators changed status" in line:
            in_gen_status_changes = False
        elif in_gen_status_changes:
            ret = parse_gen_status_changes(file_in, line_num, line,\
                                           increment, snap_num, \
                                           gen_hdr_fr_to)
            if len(ret) > 1:
                gen_status_changes += [ret] 
        
         
        # Branch Status Changes
        # Sample start/stop lines
        # ========= Report on branch status changes for the period from 2016-04-27 08:00 to 2016-04-27 23:00 (EST)
        #  ========= 4315 SDX branch outage records defined
        #  =========  340 Branches changed status. 11 already applied 
        if "Report on branch status changes " in line:
            in_branch_status_changes = True
            branch_hdr_fr_to = parse_branch_hdr_fr_to(line)
        elif "SDX branch outage records defined" in line or \
             " Branches changed status. " in line:  # "SDX branch outage records defined"
            in_branch_status_changes = False
        elif in_branch_status_changes:
            ret = parse_branch_status_changes(file_in, line_num, line, \
                                              increment, snap_num, \
                                              branch_hdr_fr_to)
            if len(ret) > 1:
                branch_status_changes += [ret] 
        
        # xfmr Status Changes
        # Sample start/stop lines
        # ========= Report on 3-winding transformers status changes for the period from 2016-04-22 08:00 to 2016-04-22 23:00 (EST)
        # =========  128 3-winding transformers SDX outage records defined
        # ========= Report on 3-winding transformers status changes for the period from 2016-04-20 08:00 to 2016-04-20 23:00 (EST)
        # ========= No 3-winding transformers changed status for the period from 2016-04-20 08:00 to 2016-04-20 23:00 (EST)
 
        if "Report on 3-winding transformers status changes " in line:
            in_xfmr_status_changes = True
            xfmr_hdr_fr_to = parse_xfmr_hdr_fr_to(line)
        elif "3-winding transformers SDX outage records defined" in line or \
             " 3-winding transformers changed status for" in line :  
            in_xfmr_status_changes = False
        elif in_xfmr_status_changes:
            ret = parse_xfmr_status_changes(file_in, line_num, line, \
                                              increment, snap_num, \
                                              xfmr_hdr_fr_to)
            if len(ret) > 1:
                xfmr_status_changes += [ret] 

        # Summary from bottom of file
        #for match in re.finditer(created_pattern, line):
        log_dt = parse_log_date(line, log_dt)
        #if cfg.verbose: print('log_dt: ' + str(log_dt))
        #solution summary table
        if re.search(soln_summary_pattern, line):
            soln_summary += parse_soln_summary(file_in, log_dt, line_num, line, first_snap_dt)
        # soln_worst: is this iteration's solution worse than others?
        try:
            temp = int(soln_summary[-1][-1].strip()[-5])
        except: 
            temp = 0
        if temp > soln_worst: 
            soln_worst = temp
        # additional solution summary 
        if "LF models" in line and "Created" in line:
            try:
                lf_model_cnt = int(line[8:12].strip())
            except:
                lf_model_cnt = line[8:12].strip()   
        if 'Exit program' in line:
            complete_log = True

    # ----------------------------------------------------------------
    # -----------      End of file parsing Loop     ------------------
    # ----------------------------------------------------------------
    if cfg.verbose: print('soln_worst: ' + str(soln_worst))

    # create run summary   
    # run_summary=[Log_file, 'increment', 'log_date', 'lf_model_cnt', 'complete_log', 'worst_solution']
    run_summary = [file_in, increment, log_dt, \
                   lf_model_cnt, complete_log, soln_worst]
    
    if cfg.verbose: 
        parse_stop = datetime.datetime.now()
        print('---- Finished parsing: ' + str(parse_stop - parse_start) + ' ----')
        print('snapshot_def rows: ' + str(len(snapshot_def)))
        print('non-converge rows: ' + str(len(non_converge)))
        print('bus mismatch rows: ' + str(len(bus_mismatch)))
        print('bus mismatch detail rows: ' + str(len(bus_mism_dtl)))
        print('solution summary rows: ' + str(len(soln_summary)))
        print('Gen status changes: ' + str(len(gen_status_changes)))
        print('branch status changes: ' + str(len(branch_status_changes)))
        print('3-winding xfmr status changes: ' + str(len(xfmr_status_changes)))
        print('')

    if type_conv:
        if cfg.verbose: 
            print('')
            tc_start = datetime.datetime.now()
            print('---- Start data type conversion ----')
        if len(snapshot_def) > 0: 
            snapshot_def = type_fixer(snapshot_def, strip_chars=', ')
        if len(non_converge) > 0: 
            non_converge = type_fixer(non_converge, strip_chars=', ')
        if len(bus_mismatch) > 0: 
            bus_mismatch = type_fixer(bus_mismatch, strip_chars=', ')
        if len(bus_mism_dtl) > 0: 
            bus_mism_dtl = type_fixer(bus_mism_dtl, strip_chars=', ')
        if len(soln_summary) > 0: 
            soln_summary = type_fixer(soln_summary, strip_chars=', ')
        if len(gen_status_changes) > 0: 
            gen_status_changes = type_fixer(gen_status_changes, \
                                               strip_chars=', ')
        else: 
            gen_status_changes = []
        if len(branch_status_changes) > 0: 
            branch_status_changes = type_fixer(branch_status_changes, \
                                               strip_chars=', ')
        else: 
            branch_status_changes = []
        if len(xfmr_status_changes) > 0: 
            xfmr_status_changes = type_fixer(xfmr_status_changes, \
                                               strip_chars=', ')
        else: 
            xfmr_status_changes = []
        if cfg.verbose: 
            tc_stop = datetime.datetime.now()
            print('---- Finished data type conversion: ' + \
                  str(tc_stop - tc_start) + ' ----')
            print('')
    
    # Solution 3 Metadata Report (includes Soln 3 Summary)
    soln3_meta = get_soln3_meta(soln_summary)    
    if type_conv:
        if len(soln3_meta) > 0: 
            soln3_meta = type_fixer(soln3_meta, strip_chars=', ')
    ''' Returns list: [soln3_summary, before_snap3, first_snap3, last_snap3, \
                 after_snap3, snap3_cnt, snap_cnt]'''
    
    if len(soln3_meta) < 4:
        print('\n' + '*'*70)
        print(''*20 + 'Error in soln3_meta!')
        print(soln3_meta)
        print('*'*70 + '\n')
    else:
        before_snap3 =  soln3_meta[1]
        # before_snap3 = {}.fromkeys(before_snap3).keys() #return unique list
        first_snap3 =  soln3_meta[2] 
        last_snap3 =  soln3_meta[3] 
        after_snap3 =  soln3_meta[4]

        # solution 3 generation status report     
        compare_col_list = ['bus_num', 'bus_name']
        #gen_snaps = gen_status_change['snap_num'] .drop_duplicates()
        # NBext few lines are just to extract the column definition.  
        #      df1 and df2 are of no use.
        df1=gen_status_change[2]
        df2=gen_status_change[3]
        temp= pd.merge(df1, df2, how='outer',
                                 on=compare_col_list)
        gen_delta_cols=list(temp.columns)
        gen_delta = pd.DataFrame(columns=gen_delta_cols)
        
        if before_snap3 != None and first_snap3 != None:
            gen_before = gen_status_changes['snap_num'==before_snap3]
            gen_first = gen_status_changes['snap_num'==first_snap3]
            gen_delta = pd.merge(gen_before, gen_first, how='left',
                                 on=compare_col_list)
            gen_delta_cols = list(gen_delta.columns)
            gen_delta.append(pd.merge(gen_before, gen_first, how='right',
                                 on=compare_col_list))
        if last_snap3 != None and after_snap3 != None:
            gen_last = gen_status_changes['snap_num'==last_snap3]
            gen_after = gen_status_changes['snap_num'==after_snap3]
            gen_delta.append(pd.merge(gen_last, gen_after, how='left',
                                 on=compare_col_list))
            gen_delta.append(pd.merge(gen_last, gen_after, how='right',
                                 on=compare_col_list))
        if gen_delta == None:
            gen_delta = pd.DataFrame(columns=gen_delta_cols)
        '''
        # solution 3 branch status report     
        branch_change_report = []
        if before_snap3 != None and first_snap3 != None:
            branch_change_report += branches_snap1_not_2(file_in, branch_status_changes, \
                                before_snap3, after_snap3, in_snap=2)
        if last_snap3 != None and after_snap3 != None:
            branch_change_report += branches_snap1_not_2(file_in, branch_status_changes, \
                                last_snap3, after_snap3, in_snap=1)
        
        # solution 3 xfmr status report     
        xfmr_change_report = []
        if before_snap3 != None and first_snap3 != None:
            xfmr_change_report += xfmrs_snap1_not_2(file_in, xfmr_status_changes, \
                                before_snap3, after_snap3, in_snap=2)
        if last_snap3 != None and after_snap3 != None:
            xfmr_change_report += xfmrs_snap1_not_2(file_in, xfmr_status_changes, \
                                last_snap3, after_snap3, in_snap=1)
        '''

    # return results and optionally write to file(s)
    if cfg.verbose: 
        print('')
        store_start = datetime.datetime.now()
        print('---- Start lists to storage----')
    
    #         [ list       , column_specs         , filename           ]
    frames = [[run_summary,  cfg.run_summary_cols, cfg.run_summary_file], \
              [snapshot_def, cfg.snapshot_def_cols, cfg.snapshot_def_file], \
              [non_converge, cfg.non_converge_cols, cfg.non_converge_file], \
              [bus_mismatch, cfg.bus_mismatch_cols, cfg.bus_mismatch_file], \
              [bus_mism_dtl, cfg.bus_mism_dtl_cols, cfg.bus_mism_dtl_file], \
              [soln_summary, cfg.soln_summary_cols, cfg.soln_summary_file], \
              [gen_status_changes, cfg.gen_status_change_cols, cfg.gen_status_changes_file], \
              [branch_status_changes, cfg.branch_status_change_cols, cfg.branch_status_changes_file], \
              [xfmr_status_changes, cfg.xfmr_status_change_cols, cfg.xfmr_status_changes_file], \
              [soln3_meta, cfg.soln3_meta_cols, cfg.soln3_meta_file]]

              #[gen_delta, cfg.gen_delta_cols, cfg.gen_delta_file], \
    
    rets = []    
    for i in range(len(frames)):
        # List to dataframe
        try:
            df = pd.DataFrame(frames[i][0], columns=frames[i][1]) # list to dataframe
        except:            
            df = pd.DataFrame(columns=frames[i][1]) # empty dataframe of correct size
        
        # dataframe to file
        if cfg.append_date:
            file_name = file_name_fixer(str(frames[i][2]), \
                                        date_suffix=str(log_dt)[:16])
        else:
            file_name = file_name_fixer(str(frames[i][2]))
        if return_type in [1,3]:
            # file: store dataframe to file
            appnd_hdr = file_empty(file_name) #If file is empty, append header.
            with open(file_name, 'a+') as f:
                df.to_csv(f, index=False, \
                                delim_whitespace=True, header=appnd_hdr)        
        if return_type == 4:
            # sqlite_db:  store the dataframes to the sqlite_db specified int eh config file.
            ' code to store dataframes to cfg.sqlite_db '
        if return_type in [2,3,4]:
            #  dataframes: return list of dataframes
            rets += [df]   # add the dataframe to the list of returns
        if return_type == 1:
            # return boolean: True or False
            rets = True
        
    if cfg.verbose: 
        print('')
        store_stop = datetime.datetime.now()
        print('---- Finished lists to storage: ' + \
              str(store_stop - store_start) + ' ----')
        print('')
        print('---- Finished report_from_log_file().  Run time: ' + \
              str(store_stop - script_start) + ' ----')
    
    return rets # return list containing dataframes for this log file.

def del_soln_reports(pattern='AFC_report_*'):
    f_list = pf.find_files(cfg.dir_out, pattern=pattern, recursive=False)
    f_list =[os.path.join(cfg.dir_out, f) for f in f_list]
    return pf.delete(f_list, silent=True)
    
# -------------------------------------------------------------------
# The one function that rules them all.
# -------------------------------------------------------------------
def soln_reports(from_server=False, soln_level=0, \
                 type_conv=False, return_type=3):

    soln_reports_start = datetime.datetime.now()
    if cfg.verbose: print('\n------------------------------------------------------------'*3)
    print('|--------------- Starting soln_reports ---------------|')
    if cfg.verbose: print('|----------------------------------------------------------|/n')
    
     # initialize
    #global soln_rpt
    soln_rpt=[]
	# Find the log files
    log_file_list = pf.find_files(root_path=cfg.dir_server, \
                               pattern=cfg.regex_file_pattern, \
                               recursive=False) # get list of log files
    server_file_list = [os.path.join(cfg.dir_server, fname) for fname in log_file_list]
    working_file_list = [os.path.join(cfg.dir_working, fname) for fname in log_file_list]
    # copy the files to dir_working
    soln_rpt=[]
    for file_num in range(len(server_file_list)):
        try:
            srv_file = server_file_list[file_num]
            wrk_file = working_file_list[file_num]
        except:
            if cfg.verbose: print('Unexpected Error')
            return [-1,'Error.  Unable to read from file list.']
        if from_server: 
            try:
                os.remove(wrk_file)
                if cfg.verbose: print("deleted old file : " + str(wrk_file))
            except:
                "do nothing"
            try:
                shutil.copy(srv_file, cfg.dir_working)
                if cfg.verbose: print("copied: " + str(srv_file) + \
                                      " to " + str(wrk_file)    )
            except:
                return [-2,'Unable to copy log file from server to working directory.']
        else:
            if cfg.verbose: print("using files in working directory")

        soln_rpt += [report_from_log_file(wrk_file, type_conv=type_conv, \
                     return_type=return_type)]
    
    soln_reports_stop = datetime.datetime.now()
    tot_time = soln_reports_stop -soln_reports_start
    if cfg.verbose: print('\n------------------------------------------------------------')
    print('|--------------- Finished soln_reports ---------------|')
    if cfg.verbose: print(2*'------------------------------------------------------------\n')
    print('         run time = ' + str(tot_time))
    
    return soln_rpt


# -------------------------------------------------------------------
# allow execution as command line script: python soln3_fixer.py
# -------------------------------------------------------------------
if __name__ == "__main__":
    #def read_config(cfg_file = 'soln3_fixer.cfg'):
    '''
    read_config - reads in configuration file if run from command line
    Default execution is of soln3_fixer.cfg in current directory.  All
    items from read_config are set to global variables.

    The soln3_fixer.cfg file is expected in:
    {python install folder}\Lib\site-packages\psyops\soln3_fixer.cfg.
    
    '''
    print del_soln_reports()
    ret =  soln_reports(False, soln_level=0, type_conv=False, return_type=3) 
    
#print('soln3_fixer(True)')
#soln3_fixer(False,)