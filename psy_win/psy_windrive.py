
# ********** FOR WINDOWS ONLY  **********  

# adapted from 	http://stackoverflow.com/questions/2625877/copy-files-to-windrive-path-or-drive-using-python
#the two NET USE commands come in pair and the second one should always be executed when the first one was executed (even if an exception was raised somewhere in between)

# map_windrive() maps a Windows network share to a drive 
# Returns: drive letter if succeeds, None if fails
def map_windrive(share, username=None, password=None, drive_letter=''):
    if drive_letter=='' or is_windrive_mapped(drive_letter):
        drive_letter=unmapped_windrives()[-1]
    cmd_parts = ["NET USE %s: %s" % (drive_letter, share)]
    if password:
        cmd_parts.append(password)
    if username:
        cmd_parts.append("/USER:%s" % username)
        os.system(" ".join(cmd_parts))
    try:
        return drive_letter
    except:
        return None

# unmaps a windrive drive
def unmap_windrive(drive_letter):
    try:
        os.system("NET USE %s: /DELETE" % drive_letter)
        return drive_letter
    except:
        return None

# returns list of unmapped drives
def unmapped_windrives(letters_only=True):
    import os, string
    try:
        ret_list = ['%s:' % d for d in string.ascii_uppercase if not os.path.exists('%s:' % d)]
        if letters_only:
            for x in range(len(ret_list)): ret_list[x]=str(ret_list[x])[0]
        return ret_list
    except: return None

# returns list of mapped drives
def mapped_windrives(letters_only=True):
    import os, string
    try:
        ret_list =  ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        if letters_only:
            for x in range(len(ret_list)): ret_list[x]=str(ret_list[x])[0]
        return ret_list
    except: return None

# alternative version of mapped_windrives() using win32api 
def mapped_windrives_alt(letters_only=True):
    try:
        import win32api
        if letters_only:
            return win32api.GetLogicalDriveStrings().replace(':\\', '').split('\000')[:-1]
        else:
            return win32api.GetLogicalDriveStrings().split('\000')[:-1]
    except:
            return None
        
# Returns first available drive letter, alphabetically 
def first_unmapped_windrive(letter_only=True):
    return unmapped_windrives(letter_only)[0]

# Returns last available drive letter, alphabetically 
def last_unmapped_windrive(letter_only=True):
    return unmapped_windrives(letter_only)[-1]

# Returns True if drive letter available, False if unavailable (already in use)
def is_windrive_mapped(drive_letter):
    try: return drive_letter.snip()[0] in mapped_windrives(True)
    except: return None

# windrive_cntxt_mgr() 
# Use with last_unmapped_windrive() or unmapped_windrives()[-1]
# to take action on folders and files on a Windows windrive drive.
from contextlib import contextmanager
@contextmanager
def windrive_cntxt_mgr(share, username=None, password=None, drive_letter = ''):
    """Context manager that mounts the given share using the given
    username and password to the given drive letter when entering
    the context and unmounts it when exiting."""
    drive_letter=map_windrive(share, username, password, drive_letter)
    try:
        yield 
    finally:
        unmap_windrive(drive_letter)

# Example 1 of windrive_cntxt_mgr
def windrive_cntxt_mgr_example1():
    drive_letter=unmapped_windrives()[-1]  # find last unused drive letter, alphabetically
    fr_path = str(drive_letter) + r":\etools\deployments\afcatc\application.properties"  # file to copy.  In this example, copying from windrive share
    to_path = r'C:\temp\delete.me2' # file to copy.  In this example, copying TO local drive
    with windrive_cntxt_mgr(r"\\corp.pjm.com\shares\special\Common", None, None, last_unmapped_windrive()):
        import shutil
        shutil.copyfile(fr_path, to_path) # copy file using windrive_cntxt_mgr() & shutil.copyfile
    # on exit of 'with windrive_cntxt_mgr()' the network drive is automatically unmapped!

# Example 2 of windrive_cntxt_mgr
def windrive_cntxt_mgr_example2():
    # windrive share properties
    ntwk_path = r"\\corp.pjm.com\shares\special\Common"      # windrive path for "I:\Common"
    username = None  # login is via Active Directory (AD) authentication.  Do not provide ID & PW via script
    password = None 
    drive_letter=unmapped_windrives()[-1]  # find last unused drive letter, alphabetically
    
    # file properties
    fr_path = str(drive_letter) + r":\etools\deployments\afcatc\application.properties"  # file to copy.  In this example, copying from windrive share
    to_path = r'C:\temp\delete.me2' # file to copy.  In this example, copying TO local drive

    # copy file using windrive_cntxt_mgr() & shutil.copyfile
    with windrive_cntxt_mgr(ntwk_path, username, password, drive_letter):
        import shutil
        shutil.copyfile(fr_path, to_path)

# Example of map_windrive and unmap_windrive
def copy_files_w_maped_windrive_example():
    try:
        # map windrive drive (2n parameter missing, so use any drive letter available starting with Z)
        drive_letter = map_windrive(r"\\corp.pjm.com\shares\special\Common")
        if len(drive_letter)<1: return None #only continue if found an available drive letter

        # specify from and to path+file
        from_file = str(drive_letter) + r"\etools\deployments\afcatc\application.properties"
        to_file = r'C:\temp\delete.me1'

        # copy file(s)
        import shutil
        shutil.copyfile(fr_path, to_path)
    except:
        return None
    finally:
        unmap_windrive(drive_letter)
    


