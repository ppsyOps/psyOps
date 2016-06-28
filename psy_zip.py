'''
zippy is a python extension of zip funtionality.

    
'''
# _____________________
#    Functions
# _____________________
def find_in_zip(zip_filename, find_file, case_sensitive=False):
	'''
	# find_in_zip() finds all files in the zip_filename that
	    # are are named like find_in_file.
	# Returns list of filenames matching find_file criteria.
	# parameters:
	    #zip_filename: the name of the zip file to be searched
	    #find_file: name of file(s) to find.  Wildcards, like "*.txt" permitted.
	    # case_sensitive: True or False
	'''
    # get list of files from zip_filename
    import zipfile as z 
    z_file = z.ZipFile(zip_filename.strip(), 'r') # load zip file
    file_list = z_file.namelist() # get file list from zip file
    z_file.close()

    # ceate match_list of filenames like find_file
    import fnmatch
    match_list=[]
    find_file = find_file.strip()
    if not case_sensitive:
        find_file=find_file.lower()
    for fn in file_list:  #fn = filename from zip file
        fn=str(fn)
        if not case_sensitive: fn2 = fn.lower()
        if fnmatch.fnmatch(fn2, find_file):
            match_list+=[fn]

    # return the filtered list of filenames
    return match_list


def is_in_zip(zip_fn, archive_fn, case_sensitive=False):
    '''
    # returns True if zip_fn exists in zipped_file
    # else returns false
	'''
    import zipfile as z  # import methods
    z_file = z.ZipFile(zip_fn, 'r') # load zip file
    file_list = z_file.namelist() # get file list from zip file
    z_file.close()
    if case_sensitive:
        temp_list = [elem for elem in file_list if archive_fn == elem]
    else:
        temp_list = [elem for elem in file_list if archive_fn.lower() == elem.lower()]
    if len(temp_list)>0:
        return True
    else:
        return False

def csv_from_zip(zip_fn, csv_fn):
	'''
	#csv_from_zip() reads a single csv file from inside
    # a zip File and returns an 2D list (array) of
    # the file content
    # Parameters:
        # zip_fn is the name of the zip file (including path)
        # csv_fn is the name of the csv file in the zip
	'''
    try:
        import zipfile
        archive = zipfile.ZipFile(csv_fn, 'r') 
        csv_data = archive.read(csv_fn)
        archive.close()
        return csv_data
    except:
        return []


def query_zips(path, recursive=False, \
               archived_file_name='C:\temp\out.csv', \
               where_clause='', \
               header_row=[], date_fmt='%d/%m/%Y %H:%M:%S', \
               csv_out_name=''):
	'''
	query_zips() function
	Searches each zip found in path,
	finds archived_file_name in each zip,
	returns that data to a 2d list    ret=[]
	'''
    success=True
	import psypy
    # get list of zip files
    zfn_list = find_files(path, '*.zip') #zip filename list
    print 'zip files: ' + str(zfn_list)
    print
    # for each zip file, extract a single, target file
    for i in range(len(zfn_list)):
        try:
            # extract the csv to a 2D list
            csv_data = csv_from_zip(zfn_list[i], archived_file_name)
        except:
            print str(zfn_list[i]), ' has no file: ', str(archived_file_name)
        if csv_out_name='':
            success = success and \
                      query_list(csv_data, where_clause,\
                                 header_row, 100, csv_out_name,\
                                 'a',False)
        else:
            ret += psypy.query_list(csv_data, where_clause,\
                              header_row, 100, csv_out_name,\
                              'a',False)
    if csv_out_name='':
        return success
    else:
        return ret

# _____________________
#    Testing
# _____________________
def query_zips_test():
    path = r'\\corp.ds.pjm.com\shares\atc\ATC_Archives\Aug_2015'
    recursive=False
    archived_file_name = 'PJM_atc_hourly_nfirm_wpc.csv'
    where_clause = 'Path=='+'"NYIS-PJM"'
    header_row=['ATC','Start','Stop','Calculator','Path','Product','Calc_Time','Limiting FG','Dfax','ResImp','C10','C11','C12','C13','C14']
    date_fmt='%d/%m/%Y %H:%M:%S'
    csv_out_name = r'C:\temp\out.csv'
    
    query_zips(path, recursive,\
               archived_file_name, \
               where_clause,\
               header_row, date_fmt, \
               csv_out_name)





def find_in_zip_test():
    print 'Test find_in_zip "CSV*"'
    temp_list = find_in_zip('C:/temp/temp.zip', 'CSV*')
    print temp_list
    print ''

    print 'Test find_in_zip "*.py"'
    temp_list = find_in_zip('C:/temp/temp.zip', '*.py')
    print temp_list
    print ''
	



def query_zips_test():
    path = r'\\corp.ds.pjm.com\shares\atc\ATC_Archives\Aug_2015'
    recursive=False
    archived_file_name = 'PJM_atc_hourly_nfirm_wpc.csv'
    where_clause = 'Path=='+'"NYIS-PJM"'
    header_row=['ATC','Start','Stop','Calculator','Path','Product','Calc_Time','Limiting FG','Dfax','ResImp','C10','C11','C12','C13','C14']
    date_fmt='%d/%m/%Y %H:%M:%S'
    csv_out_name = r'C:\temp\out.csv'
    
    query_zips(path, recursive,\
                   archived_file_name, where_clause,\
                   header_row, date_fmt\
                   , csv_out_name)


