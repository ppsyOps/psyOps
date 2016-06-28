# File:"C:\Python27\Lib\site-packages\psyops\psse_compare.py", generated on TUE, APR 26 2016  14:20, release 32.02.02

##################################################################
#                        Initialize
##################################################################
import pssepath
pssepath.add_pssepath()
import psspy
import os

compare_opt = \
{'bus identifiers':1 ,'bus type codes':2, \
 'machine status':3, 'generator MW':4, \
 'generator MW or MVAR':5, 'bus loads':6, \
 'bus shunts':7, 'switched shunts':8, \
 'voltage':9, 'voltage and angle':10, \
 'Mbase and Zsorce':11, 'Mbase and Zpos':12, \
 'Mbase and Zneg':13, 'Mbase and Zzero':14,  \
 'negative sequence bus shunts':15, 'zero sequence bus shunts':16,  \
 'branch status':17, "line R:'X:'B":18,  \
 'line shunts':19, 'line ratings':20,  \
 'metered end':21, 'transformers':22,  \
 'flow MW or MVAR (from bus)':23, 'flow MW or MVAR (from & to)':24,  \
 'line MW or MVAR losses':25, "zero sequence R:'X:'B":26,  \
 'zero sequence line shunts':27, 'connection codes':28,  \
 'zero sequence mutuals':29, 'multi-section lines':30,  \
 'multi-section metered end':31, 'load status':32,  \
 'line lengths':33, 'generator MVAR':34,  \
 'flow MW (from bus)':35, 'flow MVAR (from bus)':36,  \
 'flow MW (from and to)':37, 'flow MVAR (from and to)':38,  \
 'line MW losses':39, 'line MVAR losses':40,  \
 'fixed bus shunt status':41, 'switched shunt status':42,  \
 'scalable load flag':43}

##################################################################
#                        User Input
##################################################################

case1_file=r"""C:\temp\sum16idctr1p4_v32.sav"""
case2_file=r"""C:\temp\sum16idctr1p6_v32.sav"""

#Set comparison to run.  For all comparisons, set
# comparisons=compare_opt
comparisons=['bus identifiers','generator MVAR']

pjm_list=[40,39,34,42,41,44,28,30,35,26,\
           38,29,27,32,36,33,31,37,43]
area_list=pjm_list

##################################################################
#                           Begin
##################################################################

#def compare(case1=case1_file,case2=case2_file,areas)
# Prompt for cases to compare.  First case can be .raw or .sav.  Second case
# must be .sav.
print('Compare PSS/e cases.  The first case can be .raw or .sav.  ' + \
      '\nThe second case must be .sav.')
msg='Please enter the path/file.ext for the first case (.raw or .sav) file:'
while not os.path.isfile(case1_file):
    case1_file=input(msg)
    msg="Sorry, I can't find " + case1_file + ".  Try again."

msg='Please enter the path/file.ext for the second saved case (.sav) file:'
while not  os.path.isfile(case2_file):
    case2_file=input(msg)
    msg="Sorry, I can't find " + case1_file + ".  Try again."

#open a case
psspy.case(r"""C:\temp\sum16idctr1p4_v32.sav""")

# define a susbsytem to compare
# bsys() batch defines a bus subsystem 
ierr =psspy.bsys(0,0,[ 0.2, 999.],19,area_list,0,[],0,[],0,[])
if ierr != 0:
    print('Error defining subsystem.')

#Initialize
SID = 0      # subsystem identifier, 0 by default\
All = 0      # 1 = all busses; 0 = busses in subsystem\
APIOpt = 1   # 1 = inititalize, 2 = run comparison, 3 = done (cleanup)
Status = [0,0,0,0],   # List of 4 items.  see help['psspy.diff']
Thrsh = [0.0,0.0,0.0]  # thrsh1: difference threshold (default = 0)
#                      thrsh2: voltage or tap ratio threshold (default = 0)
#                      thrsh3: angle threshold (default = 0)
CFile = case1_file     # PSS/e case file
ierr,seqflg = psspy.diff(SID,All,APIOut,Status,Thrsh,case1_file)

#Run comparisons
ret = []
APIOpt = 2   # 1=inititalize, 2=run comparison, 3=done (cleanup)
for i in comparisons:
    ierr,seqflg = psspy.diff(SID,All,APIOut,[0,i,0,0],Thrsh,case2_file)
    ret += [ierr, seqflg]

#Cleanup
APIOpt = 3   # 1=inititalize, 2=run comparison, 3=done (cleanup)
ierr,seqflg = psspy.diff(0,1,3,[0,0,0,0],[0.0,0.0,0.0],case2_file)



help = {}  # empty dictionary for help
help['psspy.diff'] = '''
psspy.diff is an API to compare a working case with a saved case (.sav).
diff must be references first with APIOPT=1, then any number of APIOPT=2 
and finally one APIOPT=3.  APIOPT=1 initializes.  APIOPT=3 performs cleanup.

*** Syntax:
   ierr,seqflg = diff(sid, all, apiopt, status, thrsh, cfile)

*** Inputs
SID=0      subsystem identifier, 0 by default\
All=0      1=all busses; 0=busses in subsystem\
APIOpt=1   1=inititalize, 2=run comparison, 3=done (cleanup)
Status=[0,0,0,0],   List of 4 items.  If APTOpt=1, then:
                    If APTOpt=1 (initialize)
                        status1: 0=keep working case 1 open; 1=keep 2nd case open
                        status2: match by 0=bus num, 1=bus name, 2= num and name
                        status3: 0
                        status4: 0
                    If APTOpt=2 (compare)
                        status1: diff threshold units: 0=engineering; 1=percent
                        status2: see comp_opt dictionary above.
                        status3: load characteristics: 0=tot nominal; 
                                 1=constant MVA; 2=constant current; 
                                 3=constant admittance
                        status4: line rating set: 0=all ratings; 1=RateA
                                 2=RateB, 3=RateC
                    If APTOpt=3 (cleanup)
                        status1: 0=keep working case 1 open; 1=keep 2nd case open
                        status2: 0
                        status3: 0
                        status4: 0
Thrsh=[0.0,0.0,0.0] thrsh1: difference threshold (default=0)
                       thrsh2: voltage or tap ratio threshold (default=0)
                       thrsh3: angle threshold (default=0)
CFile=case1_file    PSS/e case file

*** Outputs
SeqFlg(2) [SeqFlg1, SeqFlg2] Is an array of two elements returned when APIOPT = 1. The value of
each is as follows:
        SeqFlg(1) is true if there is sequence data in the working case.
        SeqFlg(2) is true if there is sequence data in the Saved Case in
                  file CFILE.
Integer iErr Is the error code (output).
             0 no error occurred.
             1 invalid SID value or subsystem SID is not defined.
             2 invalid ALL value.
             3 invalid APIOPT value.
             4 invalid STATUS value.
             5 invalid THRSH value.
             6 CFILE is blank.
             7 unexpected APIOPT value.
             8 error building the case to case translation files.
             9 error reading the comparison case.
             10 prerequisite requirements for API are not met.
'''
