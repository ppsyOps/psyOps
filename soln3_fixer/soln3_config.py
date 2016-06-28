# soln3_fixer.cfg contains settings for the soln3_fixer.py script

# ---------------------------------------------------------------------------
#                    ----------- Instructions -----------                   
# ---------------------------------------------------------------------------
#
# At a minimum, review and update the following settings:
#     soln_num, dir_server, dir_server, and dir_out
#
# Comments must start with # as the first character position 
# and must be on a separate line from settings.
#
# Use a back slash (\) to continue a statement on the next line.
#
# Use forward slash (/) in paths instead of back slash.
#
# psyops library must be installed (see Chris Advena) for soln3_fixer to
# function properaly.  


# ---------------------------------------------------------------------------
#                          Prefernces
# ---------------------------------------------------------------------------
# Dump more print() statements to the python console.
global verbose
verbose = True

# Take extra time to attempt to convert all the parsed data from strings
# to proper python data types.  Exptect this to extend processing time.
global type_conv
type_conv = False

# ---------------------------------------------------------------------------
#                          Report filter criteria
# ---------------------------------------------------------------------------
# Regular expression to identify rows in the solution summary table (located  
#   near the end of the log file)
# Begin DO NOT CHANGE
# set 
#    soln_num = 0 for all solutions
#    soln_num = 1 for solution 1 only
#    soln_num = 2 for solution 2 only
#    soln_num = 3 for solution 3 only
global soln_num
soln_num = 0

# Location of the psyops python library.  See Chris Advena.
# located on network share: "//corp/shares/TransmissionServices/TSD, Shared Interest/Misc/Code/Python/psyops"
global psyops_path  #used under Misc section at the bottom.
psyops_path = r'c:/python27/lib/site-packages/psyops'
# psyops_path = r"//corp/shares/TransmissionServices/TSD, Shared Interest/Misc/Code/Python/psyops"


# ---------------------------------------------------------------------------
#                              Directories
# ---------------------------------------------------------------------------

# Source directory where ATC log files are stored
#     dir_server = '//Oas02awp/pti/ATCPJM/log'  
#     dir_server = 'K:/AFC Model Solution Logs/log'
global dir_server  
dir_server = r'c:/temp'  #r'K:/AFC Model Solution Logs/log'

# Temporary directory used by soln3_fixer.py script.
# r'c:/temp/', r'K:/AFC Model Solution Logs', etc.
global dir_working
dir_working = r'c:/temp/'

# output directory for output to be saved.
# r'c:/temp/', r'K:/AFC Model Solution Logs', etc.
global dir_out
dir_out = dir_working    

# directory where output will be saved
# filename only, no path     
global file_out
file_out = 'AFC Solutions Report.csv'  

# ---------------------------------------------------------------------------
#                              File Names
# ---------------------------------------------------------------------------
#   !!!! I recommend you do NOT place an extension in
#        the filenames below.  If extension is included,
#        and append_date = True, you will have one messed
#        up filename                        .             !!!!
global append_date  #append date to filename?
append_date = False
global ext
ext = 'csv'
global run_summary_file
run_summary_file = "AFC_report_run_summary"
global snapshot_def_file
snapshot_def_file = "AFC_report_snapshot_def" 
global non_converge_file
non_converge_file = "AFC_report_non_converge"
global bus_mismatch_file
bus_mismatch_file = "AFC_report_ bus_mismatchv"
global bus_mism_dtl_file
bus_mism_dtl_file = "AFC_report_bus_mismatch_detail"
global soln_summary_file
soln_summary_file = "AFC_report_solution_summary"
global soln3_meta_file
soln3_meta_file = "AFC_report_solution3_metadata"
global gen_status_changes_file
gen_status_changes_file = "AFC_report_gen_status_changes"
global branch_status_changes_file
branch_status_changes_file = "AFC_report_branch_status_changes"
global xfmr_status_changes_file
xfmr_status_changes_file = "AFC_report_xfmr_status_changes"
global gen_delta_file
gen_delta_file = "AFC_report_gen_delta"
global branch_delta_file
branch_delta_file = "AFC_report_branch_delta"
global xfmr_delta_file
xfmr_delta_file = "AFC_report_xfmr_delta"

global sqlite_db
sqlite_db = dir_out + "/afcatc.sqlite3"

# ---------------------------------------------------------------------------
#                              RegEx filters
# ---------------------------------------------------------------------------
# Filter pattern (regex) for collecting the log files from dir_server
# regex_file_patternoptions  'h*log_*ly.txt' , 'd*log_*ly.txt' , 
#                            'w*log_*ly.txt' , 'm*log_*ly.txt' ,
#                            'y*log_*ly.txt' , '*log_*ly.txt'
global regex_file_pattern
regex_file_pattern = '*log_*ly.txt'   

global regex_created_pattern
regex_created_pattern = "Created -*TARA Ver"

# soln_summary_pattern must be a regular expression (regex)
#global soln_summary_pattern
#soln_summary_pattern = r'\d\d\ amb_solve\d\.dir'

# ---------------------------------------------------------------------------
#                               Simple filters
# ---------------------------------------------------------------------------

global snapshot_def_substr
snapshot_def_substr = r"------------------ Creating snapshot "

global non_converge_substr
non_converge_substr = r". Fast Dec LF didn't converge in "

global bus_mism_dtl_substr
bus_mism_dtl_substr = r"******************* Detailed bus flow analysis for"

global log_date_substrs
log_date_substrs = [" Created - ", " TARA Ver "]
# ---------------------------------------------------------------------------
#                            Column headers
# ---------------------------------------------------------------------------

# The 16 column headers for the solution summary table.
# recommended: soln_summary_cols = ['Increment', 'Interval','Iterations','Pms','Qms',\
#             'P_Mismatch','P_Bus#','P_BusName','P_Volt','P_VoltMagPU',\
#             'QmaxMism','Q_Bus#','Q_BusName','Q_Volt','Q_VoltMagPU',\
#             'Solution Attempt']
# alternative: "soln_summary_cols= None" # to auto-calc column widths.
global snapshot_def_cols
snapshot_def_cols = ['log_file', 'Log_date', 'log_line', \
                     'increment', 'snapshot_num', \
                     'snap_date', 'snap_hr']

global non_converge_cols
non_converge_cols = ['log_file', 'Log_date', 'log_line', \
                     'increment', 'snapshot_num', \
                     'snap_date', 'snap_hr', \
                     'num_iterations', 'tot_mismatch', \
                     'mismatch_bus_count', 'tolerance']

global bus_mismatch_cols
bus_mismatch_cols = ['log_file', 'Log_date', 'log_line', \
                     'increment', 'snapshot_num', \
                     'snap_date', 'snap_hr', \
                     'ibus', 'Bus_Num', 'Bus_Name', 'Volt', \
                     'Area_Num', 'Zone_Num', 'Mismatch_Magnitude', \
                     'P_Mismatch', 'Q_Mismatch', 'V_Magnitude', \
                     'V_Angle', 'V_Low', 'V_OK', 'V_High']

global bus_mism_dtl_cols                     
bus_mism_dtl_cols = ['log_file', 'Log_date', 'log_line', \
                     'increment', 'snapshot_num', \
                     'snap_date', 'snap_hr', \
                     'Bus_Num', 'Bus_Name', 'Volt', \
                     'Area', 'Zone', 'CKT', 'St', 'MW', 'MVAR', 'MVA', \
                     'V_mag_[PU]', 'V_mag_[kV]', 'V_angle', 'Bus_Type', \
                     'V_Type', 'Type', 'Tap_R', 'PS_Angle', 'TAP_R_To', \
                     'branch_R', 'branch_X', 'branch_Chr', 'Rate_A', 'Rate_B', \
                     'Rate_C', 'Metered', 'Length', 'Reg_Min', 'Reg_Max', \
                     'Target_Min', 'Target_Max', 'MW_metered  MVAR_metered', \
                     'MVA_metered', 'MW_loss', 'MVAR_loss']

global soln_summary_cols
soln_summary_cols = ['log_file', 'Log_date', 'log_line', \
                     'increment', 'snapshot_num', \
                     'snap_date', 'snap_hr', \
                     'iterations', 'Pms', 'Qms', 'P_Mismatch', 'P_Bus_Num', \
                     'P_Bus_Name', 'P_Volt', 'P_Volt_Mag_PU', 'Qmax_Mismatch','Q_Bus#', \
                     'Q_Bus_Name', 'Q_Volt', 'Q_Volt_Mag_PU', 'Solution_Attempt']

global gen_status_change_cols
gen_status_change_cols = ['log_file', 'Log_date', 'log_line', \
                 'snap_num', 'report_from', 'report_to', \
                 'bus_num', 'bus_name', 'V', 'area', 'zone', 'id', \
                 'base_case_MW', 'base_case_st', 'P_min', 'P_max', 'status_type', \
                 'new_set_point', 'from_dt', 'to_dt']

global branch_status_change_cols
branch_status_change_cols = ['log_file', 'Log_date', 'log_line', \
                 'snap_num', 'report_from', 'report_from', \
                 'bus_num_fr', 'bus_name_fr', 'v_fr', 'area_fr', 'zone_fr', \
                 'bus_num_to', 'bus_name_to', 'v_to', 'area_to', 'zone_to', \
                 'ckt', 'market', 'rate_a', 'rate_b', 'rate_c', \
                 'status_type', 'base_case_st', \
                 'new_rate_a', 'new_rate_b', 'new_rate_c', \
                 'from_dt', 'to_dt' ]

global xfmr_status_change_cols
xfmr_status_change_cols = ['log_file', 'Log_date', 'log_line', \
                 'snap_num', 'report_from', 'report_from', \
                 'trnsfrmr_name', \
                 'w1_bus_num', 'w1_bus_name', 'w1_v', \
                 'w1_bus_num', 'w2_bus_name', 'w2_v', \
                 'w1_bus_num', 'w3_bus_name', 'w3_v', \
                 'ntrl_bus_num', 'star', 'nmvl', 'ckt', \
                 'status_type', 'action', \
                 'from_dt', 'to_dt' ]

'''
 ========= Isolated buses that will be shutdown
   Ind  Islnd    Bus# BusName      Volt Area Zone BTyp      PGen  PloadNom   MWShunt 
 ----   Total    83 buses                         10035.3     642.0       0.0 
 
 ***** SDX Load forecast snapshot 14 for the period 2016-04-22 00:00 Fri to 2016-04-23 00:00 Sat(EST)
 Area  AreaName      SubSysName           AMBLoad_MW GrossLoad  CurPhysLd    Delta
========= Total 34 areas with block dispatch. 31 have load forecast defined

 WarnID-5516-3-3691 Not enough generation for area  215  DUQ           Desired Dispatch     2388.7 exceeds Pmax=   2244.3. Load Decreased by     144.4

Warning-  5516 Total-     4 Level-        1 Not enough generation in area. Desired Dispatch exceeds Pmax. Load Decreased   

 Total 7 external areas

 Swing bus dispatch summary
   Bus# BusName      Volt Area AreaName      Zon ZoneName      DispChan   curPGen  PrevPGen   MinPGen   MaxPGen   curQGen   MinQGen   MaxQGen  VltSched 
 364003 1BR FERRY N3 22.0  347 TVA          1360 MUSCLE SHOAL   -140.60   1028.90   1169.50   1112.00   1169.50     35.56   -150.00    300.00    1.0400 
 Total Swing Dispatch change =    -140.60

'''

global run_summary_cols 
run_summary_cols = ['log_file', 'increment', 'log_date', 'lf_model_cnt', \
                    'complete_log', 'worst_solution']

global soln3_meta_cols
soln3_meta_cols = ['soln3_summary', 'snap_before', 'first_snap3', 'last_snap3', \
                 'snap_after', 'snap3_cnt', 'snap_cnt']


# ---------------------------------------------------------------------------
#                            Misc
# ---------------------------------------------------------------------------
# Import required psyops library, so that soln3_fixer will work.
import sys
sys.path.append(psyops_path)  # psyops_path defined up top.
global psyops
import psyops   # Used in soln3_fixer.py, which runs/requires the psyops library.
global incr_dict
incr_dict = {'h':'hour', 'H':'hour48', 'd':'day', \
             'w':'week', 'm':'month', 'y':'year' }

# ---------------------------------------------------------------------------
#                      Constants.  Do NOT edit.
# ---------------------------------------------------------------------------
global ret_bool
ret_bool = 1    # output to file, return True/False
global ret_df
ret_df = 2      # return log info as list of dataframes
global ret_both
ret_both = 3    # outpur to file and return log info as list of dataframes
global ret_sqlite
ret_sqlite = 4  # output to sqlite database file