'''
Python developers, I suggest adding the full init_psspy function to to top of code you will distribute:
import sys
sys.path.append('C:/Python27/Lib/site-packages/psyops')
import pssepathalt
psy_psse.init_psspy
'''

'''
Alternatively, you can use just the 5 lines directly below, but it is less likely to work.
# for PSSE 32 and Python 2.5
	#import sys
	#sys.path.append(r'C:\Program Files (x86)\PTI\PSSE32.2.2\PSSBIN') # dbl-check path
	#import psspy
	#import redirect
	#redirect.psse2py()

# for PSSE 34 and Python 2.7
	#import sys
	#sys.path.append(r'C:\Program Files (x86)\PTI\PSSE34\PSSBIN') # dbl-check path
	#import psspy
	#import redirect
	#redirect.psse2py()
'''

'''
# init_psspy()
    # 1. Confirms user has required PSS/e version installed.
    # 2. Confirms user is running version of Python
    #    required
    # 3. Initializes Python for PSSE interaction.
# Returns list of [code, remark]
    #code:
        # + value = success
        # - value = error
    #remark: informational remark such as failure reason.
# Parameters (inputs)
    # psse_ver_req: PSSE version required for this
    #       script to function properly.
    #       valid values are integers: 31, 32, 33, 34.
    # control_psse: 
    #       True: issue command: redirect.redirect.psse2py().
    #       False: do not issue the psse2py() command.

'''
def init_psspy(psse_ver_req=0, control_psse=True \
               , pti_path='C:\\Program Files (x86)\\PTI' \
               , bug_prt=False):
    import sys, os
    errs=[]
    # run compatibility check?
    check_result=[1,'PSS//e and Python versions are compatible. ']   # check passed until proven to failed
    cont=True
    if psse_ver_req==0:
        check_result=[2,'Compatibility check declined. ']
        cont=False     # skip compatibility check 
    # ----- Start: Check user PSSE and PY versions for compatibility) -----
    # initialize variables
    psse_py = [[31,2.5],[32,2.5],[33,2.7],[34,2.7]] # psse/py compatibility
    # validate psse_ver_req parameter: is it a number
    if cont:        
        try:
            psse_ver_req=int(float(psse_ver_req))
            type(psse_ver_req)
        except:
            cont=False
            check_result=[-1,'psse_ver_req must be a version number from 31 to 34. ']
            if bug_prt: print check_result
    # validate psse_ver_req parameter: is it in the psse_py compatability list
    if cont:
        cont=False     # don't cont compatibility check 
        for i in range(len(psse_py)):
            if psse_py[i][0]==psse_ver_req:
                cont=True
        if not cont:
            check_result=[-1,'psse_ver_req must be a version number from 31 to 34. ']
            if bug_prt: print check_result
    py_ver=0
    # get version number for python instance running now (sys.version command)
    if cont:
        try:
            py_ver = str(sys.version).split(' ')[0].split('.') #extract version from beginning of string
            py_ver = float(str(py_ver[0])+'.'+str(py_ver[1])) # keep only 1 level of subversioning, e.g., keep 2.5 from 2.5.3
            if bug_prt: print 'set py_ver:', py_ver
        except:
            print r'Warning: init_psspy() had trouble determining python version number.'

        cont = False
        for i in range(len(psse_py)):
            if py_ver==psse_py[i][1]: cont=True
        if not cont:
            check_result=[-1,'Python version ' + str(py_ver) +' not compatible. ']
            if bug_prt: print check_result
    if bug_prt: print 'py_ver', py_ver        
    # Find PSS/e installations 
    if cont:
        # pti_path folder exists?
        if bug_prt: print 'Checking pti_path:', pti_path
        if not os.path.isdir(pti_path):
            check_result=[-3,r'Unable to find PSS/e installation folder "' + pti_path + '" on this computer. ']
            if bug_prt: print check_result
            print check_result
            cont = False
    # Find PSS/e folder(s)
    if cont:
        try:
            psse_paths = os.listdir(pti_path) # get all psse installation paths
            if bug_prt: print 'Found', len(psse_paths), r'PSS/e install paths: ', psse_paths
        except:
            check_result=[-4,r'Unable to find PSS/e installation folder on this computer. ']
            if bug_prt: print check_result
            cont = False
    # Get installed PSS/e version numbers from path  # (e.g. path, 'C:\Program Files (x86)\PTI\PSSE32.2.2')
    if cont:
        psse_vers=[]
        psse_path=''
        for i in range(len(psse_paths)):  # check each path for psse_ver_req
            if bug_prt: print 'path',psse_paths[i]
            x=str(psse_paths[i])[4:6]
            if bug_prt: print 'path ver:', x,';   psse_ver_req:',str(psse_ver_req)
            try: x=int(x)
            except: x=0
            if 31<=x<=34 and str(psse_ver_req)==str(x):
                psse_path=psse_paths[i] # used later to load psspy library
                if bug_prt: print 'Found psse_path:',psse_path
            else:
                if bug_prt: print 'Did not find a psse_path in psse_paths:',psse_paths, 'where version = ',x
        if psse_path=='':
            check_result=[-5,r'Unable to find PSS/e installation folder on this computer. ']
            if bug_prt: print check_result
            cont = False
    # is psse / py version pair in compatibility list.
    cont = False
    if bug_prt: print 'Checking psse and python version against compatibility list.'
    for i in range(len(psse_py)):
        if bug_prt: print '   ', psse_py[i][0], psse_ver_req,  py_ver, psse_py[i][1]
        if psse_py[i][0]==psse_ver_req and py_ver==psse_py[i][1]:
            cont = True
            if bug_prt: print '   Winner - psse and python versions are compatible!'
            break
    if not cont:
        check_result=[-6,'Python version ' + str(py_ver) \
                      + r' not compatible with PSS/e version ' \
                      + str(psse_ver_req) + '. Compatibility list. '] # + str(psse_py)<-compaibility list
    # ----- Done: Check user PSSE and PY versions for compatibility) -----

    # -----      Start: Initialize python to interact with PSSE      -----
    if bug_prt: print ' Starting: Initialize python to interact with PSSE'
    if check_result[0]<1:
        if bug_prt: print r'Python - PSS/e compatibility check: ', check_result
    else:  #compatibility check passed or was skipped
        check_result=[-7,'Unexpected error initializing libraries (sys, psspy and redirect). ']
        try:
            import sys
            check_result=[-8,'Imported sys library. Failed to import psspy and redirect. ']
            s= pti_path+'\\'+psse_path+"\PSSBIN"
            sys.path.append(s)
            os.environ['PATH'] = os.environ['PATH'] + ';' +  s
            if bug_prt: print r'attempting to add to sys.path:', s
            if bug_prt: print r'sys.path:',sys.path
            if bug_prt: print r'attempting to load psspy.'
            import psspy
            check_result=[4,'Imported sys and psspy libraries. ']
            if control_psse:
                if bug_prt: print r'attempting to load redirect.'
                check_result=[-9,'Imported sys and psspy libraries. Failed to import redirect. ']
                import redirect
                if bug_prt: print r'attempting to execute: redirect.psse2py()'
                redirect.psse2py()
                check_result=[5,r'Successfully configured Python to control PSS/e. ']
                if bug_prt: print check_result
            if bug_prt: print 'init_psspy() completed successfully. ', check_result
        except:
            if bug_prt: print 'init_psspy() failed,  Code:', check_result
            if psse_ver_req==0:
                print r'init_psspy() failed.  For more info, run w/PSSE version like: init_psspy(32)'
                if not bug_prt: print 'Consider setting bug_prt=False for verbose debugging comments.'
                print r'If that doesn\'t solve your problem, check your PSSE and Pyton installations.'
                print r'Check out this onenote article for more information:'
                help_page = r'onenote:///\\corp\shares\TransmissionServices\TSD,%20Shared%20Interest\OneNote%20Notebooks\Software%20Development\Python.one#PSS/E%20library%20for%20Toad&section-id={A3CDFF46-74C6-4A36-B5F7-805ECC3539D9}&page-id={185CE924-9A62-4B5D-9921-1D2E4A30F244}&end'
                print help_page
                import urllib
                urllib.urlopen(help_page)
				
				
    return check_result
    # -----      Done: Initialize python to interact with PSSE      -----


ret = init_psspy(34)
print
print 'init_psspy result:', ret

