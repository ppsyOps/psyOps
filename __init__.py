# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Power SYstem OPeratorS, or psyOps (pronounced sigh-opps, is a package intended 
to contain core functionality and some common tools for power systems engineers 
and developers with Python.  

While psyOps contains classes and functions to extend the libraries listed.
below, many psyOps classes and functions will work without them.
    - psspy, the Siemens PTI PSS/e python library, which comes with PSS/e
    - pssepath, finds your PSS/e installation and sets up Python for 
        psspy.  pssepath is available on GitHub at 
        https://github.com/danifus/pssepath
"""

#Settings
__minimum_numpy_version__ = '1.5.0'
_online_docs_root = r'https://github.com/cadvena/psyOps'

import sys

# import psyops modules
'''
#None created yet.  The follwoing is just exmaple code:
import six
sys.modules['psyops.extern.six'] = six
sys.modules['psyops.extern.six.moves'] = six.moves
sys.modules['psyops.extern.six.moves.urllib_error'] = six.moves.urllib_error
import ply
sys.modules['psyops.extern.ply'] = ply
'''

def psy_path(file_name='psy_readme.txt'):
    import sys
    from os import listdir
    from fnmatch import filter    
    for sf in [r'Lib\site-packages\psyops', 'Lib', '']:
        try:
            ret=[]
            for base, dirs, files in os.walk(os.path.join(sys.exec_prefix, sf)):
                goodfiles = filter(files, file_name)
                ret.extend(os.path.join(base, f) for f in goodfiles)
            return ret[0][:-15]
        except:
            'try again'

def psy_import():
    import sys
    from os import listdir
    from fnmatch import filter    
    py_path = psy_path()    
    try:
        path.index(py_path)
        return True
    except:
        try:
            path.append(py_path)
            return True
        except:
            print('Unable to to import required psyops library.  Script will fail.')
            return False


# this indicates whether or not we are in psyops's setup.py
try:
    _psyops_SETUP_
except NameError:
    from sys import version_info
    if version_info[0] >= 3:
        import builtins
    else:
        import __builtin__ as builtins
    builtins._psyops_SETUP_ = False
    del version_info
    del builtins

#try:
#    from .version import version as __version__
#except ImportError:
#    # TODO: Issue a warning using the logging framework
#    __version__ = ''
#try:
#    from .version import githash as __githash__
#except ImportError:
#    # TODO: Issue a warning using the logging framework
#    __githash__ = ''


# The location of the online documentation for psyops
# This location will normally point to the current released version of psyops
#if 'dev' in __version__:
#    _online_docs_root = r'http://docs.psyops.org/en/latest/'
#else:
#    _online_docs_root = r'http://docs.psyops.org/en/{0}/'.format(__version__)


def _check_numpy():
    """
    Check that Numpy is installed and it is of the minimum version we
    require.
    """
    # Note: We could have used distutils.version for this comparison,
    # but it seems like overkill to import distutils at runtime.
    requirement_met = False

    try:
        import numpy
    except ImportError:
        pass
    else:
        major, minor, rest = numpy.__version__.split(".", 2)
        rmajor, rminor, rest = __minimum_numpy_version__.split(".", 2)
        requirement_met = ((int(major), int(minor)) >=
                           (int(rmajor), int(rminor)))

    if not requirement_met:
        msg = ("numpy version {0} or later must be installed to use "
               "psyops".format(
                   __minimum_numpy_version__))
        raise ImportError(msg)

    return numpy


if not _psyops_SETUP_:
    _check_numpy()


#from .config import ConfigurationItem
#UNICODE_OUTPUT = ConfigurationItem(
#    'unicode_output', False,
#    'Use Unicode characters when outputting values, and writing widgets '
#    'to the console.')


# set up the test command
def _get_test_runner():
    from .tests.helper import TestRunner
    return TestRunner(__path__[0])


def test(package=None, test_path=None, args=None, plugins=None,
         verbose=False, pastebin=None, remote_data=False, pep8=False,
         pdb=False, coverage=False, open_files=False, parallel=0,
         docs_path=None, skip_docs=False):
    """
    Run psyops tests using py.test. A proper set of arguments is
    constructed and passed to `pytest.main`.

    Parameters
    ----------
    package : str, optional
        The name of a specific package to test, e.g. 'io.fits' or 'utils'.
        If nothing is specified all default psyops tests are run.

    test_path : str, optional
        Specify location to test by path. May be a single file or
        directory. Must be specified absolutely or relative to the
        calling directory.

    args : str, optional
        Additional arguments to be passed to `pytest.main` in the `args`
        keyword argument.

    plugins : list, optional
        Plugins to be passed to `pytest.main` in the `plugins` keyword
        argument.

    verbose : bool, optional
        Convenience option to turn on verbose output from py.test. Passing
        True is the same as specifying `-v` in `args`.

    pastebin : {'failed','all',None}, optional
        Convenience option for turning on py.test pastebin output. Set to
        'failed' to upload info for failed tests, or 'all' to upload info
        for all tests.

    remote_data : bool, optional
        Controls whether to run tests marked with @remote_data. These
        tests use online data and are not run by default. Set to True to
        run these tests.

    pep8 : bool, optional
        Turn on PEP8 checking via the pytest-pep8 plugin and disable normal
        tests. Same as specifying `--pep8 -k pep8` in `args`.

    pdb : bool, optional
        Turn on PDB post-mortem analysis for failing tests. Same as
        specifying `--pdb` in `args`.

    coverage : bool, optional
        Generate a test coverage report.  The result will be placed in
        the directory htmlcov.

    open_files : bool, optional
        Fail when any tests leave files open.  Off by default, because
        this adds extra run time to the test suite.  Works only on
        platforms with a working `lsof` command.

    parallel : int, optional
        When provided, run the tests in parallel on the specified
        number of CPUs.  If parallel is negative, it will use the all
        the cores on the machine.  Requires the `pytest-xdist` plugin
        is installed.

    docs_path : str, optional
        The path to the documentation .rst files.

    skip_docs : bool, optional
        When `True`, skips running the doctests in the .rst files.

    See Also
    --------
    pytest.main : py.test function wrapped by `run_tests`.

    """
    test_runner = _get_test_runner()
    return test_runner.run_tests(
        package=package, test_path=test_path, args=args,
        plugins=plugins, verbose=verbose, pastebin=pastebin,
        remote_data=remote_data, pep8=pep8, pdb=pdb,
        coverage=coverage, open_files=open_files, parallel=parallel,
        docs_path=docs_path, skip_docs=skip_docs)


# if we are *not* in setup mode, import the logger and possibly populate the
# configuration file with the defaults
def _initialize_psyops():
    from . import config

    import os
    import sys
    from warnings import warn

    # If this __init__.py file is in ./psyops/ then import is within a source dir
    is_psyops_source_dir = (os.path.abspath(os.path.dirname(__file__)) ==
                             os.path.abspath('psyops') and os.path.exists('setup.py'))

    # try to import pssepath and pssypy
    try:
        import pssepath
        pssepath.add_pssepath()
        import psspy
    except:
        ret = _alt_init_psspy()
        print
        print 'init_psspy result:', ret

    def _alt_init_psspy(psse_ver_req=0, control_psse=True \
                   , pti_path='C:\\Program Files (x86)\\PTI' \
                   , bug_prt=False):
        '''
        # _alt_init_psspy is an alternative psse/python initializer in case pssepath
        # is not available.  
        # alternatively, you can use just the commented out lines of code directly 
        # below, but it is less robust than pssepath.
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
        import sys
        import os
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
                             
                             
    def _rollback_import(message):
        log.error(message)
        # Now disable exception logging to avoid an annoying error in the
        # exception logger before we raise the import error:
        _teardown_log()

        # Roll back any psyops sub-modules that have been imported thus
        # far

        for key in list(sys.modules):
            if key.startswith('psyops.'):
                del sys.modules[key]
        raise ImportError('psyops')

    if sys.version_info[0] >= 3 and is_psyops_source_dir:
        _rollback_import(
            "You appear to be trying to import psyops from within a source "
            "checkout. This is currently not possible using Python 3 due to "
            "the reliance of 2to3 to convert some of psyops's subpackages "
            "for Python 3 compatibility.")

    try:
        from .utils import _compiler
    except ImportError:
        if is_psyops_source_dir:
            _rollback_import(
                'You appear to be trying to import psyops from within a '
                'source checkout; please run `./setup.py develop` or '
                '`./setup.py build_ext --inplace` first so that extension '
                'modules can be compiled and made importable.')
        else:
            # Outright broken installation; don't be nice.
            raise


#import logging
## Use the root logger as a dummy log before initilizing psyops's logger
#log = logging.getLogger()
#if not _psyops_SETUP_:
#    from .logger import _init_log, _teardown_log
#    log = _init_log()
#    _initialize_psyops()
#    from .utils.misc import find_api_page

psy_import()