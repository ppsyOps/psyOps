'''
csvsql package by Chris Advena allows the user to retrieve data from a
csv file using a where clause very similar to SQL syntax using the 
select() function.

Function List
    clean_csv_entry()
    select()
    select_test()
    
clean_csv_entry() function
    remove leading and lagging whitespace,
    then remove leading/lagging quotation marks
'''

def select(csv_in_name, where_clause, header_row=[], \
             data_type_inspection=100, \
             date_fmt='%d/%m/%Y %H:%M:%S', \
             csv_out_name='', write_mode='w'):
		'''
		# Parameters
        # csv_in_name: csv file to interrogat; format: path/filename.ext
        # where_clause: the filters to apply.  e.g., 'Path=='+'"NYIS-PJM" and ATC>0'
        # header_row: if file conatins a header row, set this to an empty list, [].
                # else set to list including every column name like ['col1','col2','col3']
        # data_type_inspection: 0=check every entry in column when determining column type
                # {int}=check {int} rows sto determine column type.
                # default = 20
        # date_fmt: date format like '%d/%m/%Y %H:%M:%S'.  For help, see:
                # https://docs.python.org/2/library/datetime.html
                # http://www.tutorialspoint.com/python/time_strptime.htm
        # csv_out_name: if '' return list, else write to file
        # write_mode: 'w' to write, 'a' to append
		'''
    import datetime, time, csv
    from datetime import datetime
    start_time = time.time()
    print 'Starting select(' + str(csv_in_name) + ', ' + str(where_clause) + ')'
    print
    print 'where_clause:'
    print where_clause
    print
    retlist=[]
    csv_data = csv.reader(open(csv_in_name))
    csv_table = []
    # did the user provide a header as input?
    got_header = True
    if header_row == []: 
        got_header = False
    # read data to memory
    for row in csv_data:
        if not got_header:
            #if header identified yet, find it in file
            got_header = True
            header_row = row
        else:
            csv_table.append(row)
            
        # replace spaces w/ underscores in column headers
        if len(header_row) > 1:
            for i in range(len(header_row)):
                header_row[i] = header_row[i].replace(' ', '_')
        
    print 'header: '
    print header_row
    print

    # If no where clause, return all records.
    if where_clause=='': return csv_table
    
    # determine column types: string/int/float
    print 'Data Types: '
    colType = []
    for i in range(len(header_row)):
        isFloat = True
        isInt = True
        isDate = True
        # determine number of rows to check when validating column data type
        if data_type_inspection==0 or data_type_inspection>len(csv_table):
            data_type_inspection=len(csv_table)
        # loop through all rows to determine data type
        for j in range(data_type_inspection):
            s = clean_csv_entry(csv_table[j][i])
            try:
                v = float(s)
                if not v == int(v):
                    isInt = False
            except ValueError:
                isFloat = False
                isInt = False
            try:
                datetime.strptime(s, date_fmt)
                isDate = True
            except ValueError:        
                isDate = False
        colT = ''
        if isDate:
            colT = 'date'
        elif isInt:
            colT = 'int'
        elif isFloat:
            colT = 'float'
        else:
            colT = 'string'
        colType.append(colT)
        print header_row[i], colT
        
    # open output file for writing
    if csv_out_name!='':
        #csv_out = open(csv_out_name, 'w')
        csv_out = open(csv_out_name, 'a')
        csv_writer = csv.writer(csv_out, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # run the query
    for j in range(len(csv_table)):
        # assign the column variables
        for i in range(len(header_row)):
            s=clean_csv_entry(csv_table[j][i])
            # print s 
            if colType[i] == 'string':
                s = (str(header_row[i]) + '="' + s + '"')
                exec(s)
            elif colType[i] == 'date':
                s = header_row[i] + "='" + s + "'" #datetime.strptime(s, date_fmt)
                exec(s)
            elif colType[i] == 'float':
                exec(str(header_row[i]) + '=' + 'float("' + s + '")')
            elif colType[i] == 'int':
                exec(str(header_row[i]) + '=' + 'int(float("' + s + '"))')

        # output the rows matching the where_clause
        if eval(where_clause):
            retlist += [csv_table[j]]
            if csv_out_name!='':
                csv_writer.writerow(csv_table[j])
        
    # clean up
    if csv_out_name!='': csv_out.close()
    print("--- Runtime (seconds): %s ---" % (time.time() - start_time)) #the current time(time.time()) minus the start time (start_time)
    return retlist

# query_list() function
    # Parameters
        # data_table: csv file to interrogat; format: path/filename.ext
        # where_clause: the filters to apply.  e.g., 'Path=='+'"NYIS-PJM" and ATC>0'
        # header_row: to:
                # get header from file: set to empty list, [].
                # provide header as input: set to list of column names like ['ID','Name','col3']
                # create generic header: set to None
        # data_type_inspection: 0=check every entry in column when determining column type
                # {int}=check {int} rows sto determine column type.
                # default = 20
        # csv_out_name: if '' return list, else write to file
        # write_mode: 'a' to append, 'w' to write
        # in_place: default=True.  Ignored if csv_out_name!=''.
            # if True, delete rows from list that do not match where_clause
            # if True, return new list with only rows that do match where_clause
def query_list(data_table, where_clause='', header_row=None, \
             data_type_inspection=100, \
             csv_out_name='', write_mode='a',\
             in_place=True):
    import datetime, time, csv
    from datetime import datetime
    start_time = time.time()
    print 'Starting query_list()'
    print
    print 'where_clause:'
    print where_clause
    print

    # Update list in place?
    if in_place:
        # Create the ret_table as a reference to data_table.
        # Updating one updates the other.
        ret_table=data_table
    else:
        # load data_table values into new array, ret_table.
        # Updating one does NOT update the other.
        ret_table=[]
        for i in range(len(data_table)):
            ret_table[i]=data_table[i]
    
    # Address header row
    if header_row==None:
        # None indicates we are to create a header.
        header_row=['Col_1'] #this will cause the next if to go to else and auto add col names to header as needed
    if header_row == []:
        header_row=ret_table[0] #get header from 1st row of data_table
    else:
        if len(header_row)==len(ret_table[0]):
            # if header_row parameter has same number of entries as 1st column of data_table
            # then our job is easy; just insert the header row as the new first row
            if header_row!=ret_table[0]:
                data_table.insert(0,header_row) # header has correct # of entries
            else:
                print 'data_table already contains a header.'
        else:
            # insert the header_row parameter into data_table
            # and deal with header_row has too many/few column names.
            new_hdr = []
            for i in range(len(ret_table[0])):
                try:
                    new_hdr+=[header_row[i]]
                except:
                    new_hdr+=['Col_'+str(i+1)]
    # replace spaces w/ underscores in column headers
    for i in range(len(header_row)):
        header_row[i] = header_row[i].replace(' ', '_')
    print 'header: '
    print header_row
    print

    # If no where_clause, return all records.
    if where_clause=='':
        if in_place:
            data_table = ret_table  # line not needed; list already updated in place. Belts and suspenders code.  
            return True
        else:
            return ret_table
    
    # determine column types: string/int/float
    print 'Data Types: '
    colType = []
    for i in range(len(header_row)):
        isFloat = True
        isInt = True
        isDate = True
        # determine number of rows to check when validating column data type
        if data_type_inspection==0 or data_type_inspection>len(ret_table):
            data_type_inspection=len(ret_table)
        # loop through rows to determine data type
        for j in range(data_type_inspection):
            isDatetime = isDate and isinstance( ret_table[j][i], datetime)
            isFloat = isFloat and isinstance( ret_table[j][i], float)
            isInt = isInt and isinstance( ret_table[j][i], int)
            isString = isString and isinstance( ret_table[j][i], string)
            isList = isList and isinstance( ret_table[j][i], list)
            isTuple = isTuple and isinstance( ret_table[j][i], tuple)
        colT = ''
        if isDatetime: colT = 'datetime'
        elif isInt: colT = 'int'
        elif isFloat: colT = 'float'
        elif isString: colT = 'string'
        elif isinstance( ret_table[j][i], list): colT = 'list'
        elif isinstance( ret_table[j][i], tuple): colT = 'tuple'
        else: colT = 'other'
        # record column type                   
        colType.append(colT)
        print header_row[i], colT
        
    # open output file for writing
    if csv_out_name!='':
        csv_out = open(csv_out_name, 'a')
        csv_writer = csv.writer(csv_out, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # run the query
    for j in range(len(csv_table)):
        # assign the column variables
        for i in range(len(header_row)):
            s=clean_csv_entry(csv_table[j][i])
            # print s 
            if colType[i] == 'string':
                s = (str(header_row[i]) + '="' + s + '"')
                exec(s)
            elif colType[i] == 'date':
                s = header_row[i] + "='" + s + "'" #datetime.strptime(s, date_fmt)
                exec(s)
            elif colType[i] == 'float':
                exec(str(header_row[i]) + '=' + 'float("' + s + '")')
            elif colType[i] == 'int':
                exec(str(header_row[i]) + '=' + 'int(float("' + s + '"))')

        # output the rows matching the where_clause
        if eval(where_clause):
            if csv_out_name!='': #write to csv file
                csv_writer.writerow(ret_table[j])
            elif not in_place:   # add match to new list
                ret_table += [ret_table[j]]
        else: # update list in place. 
            #delete the non-matching row
            ret_table.remove[j]
        
    # clean up
    print("--- Runtime (seconds): %s ---" % (time.time() - start_time)) #the current time(time.time()) minus the start time (start_time)
    if csv_out_name!='':
        csv_out.close()
        return True
    elif in_place:
        data_table = ret_table  # line not needed; list already updated in place. Belts and suspenders code.  
        return True
    else:
        return ret_table




def csv_from_zip(zip_fn, csv_fn):
    # returns a list containing csv file data.
    # zip_fn = zip file name
    # csv_fn = csv file name (comma separated text file)
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
            ret += query_list(csv_data, where_clause,\
                              header_row, 100, csv_out_name,\
                              'a',False)
    if csv_out_name='':
        return success
    else:
        return ret


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


def find_files_test():
    print 'Non-recurive: c:\temp'
    ret = find_files(r'C:\temp', '*.*', False)
    print ret
    print
    print 'Recurive: c:\temp'
    ret = find_files(r'C:\temp', '*.*', True)
    print ret


def find_in_zip_test():
    print 'Test find_in_zip "CSV*"'
    temp_list = find_in_zip('C:/temp/temp.zip', 'CSV*')
    print temp_list
    print ''

    print 'Test find_in_zip "*.py"'
    temp_list = find_in_zip('C:/temp/temp.zip', '*.py')
    print temp_list
    print ''


def select_test():
    import os
    csv_in_name = r'C:\temp\PJM_atc_hourly_nfirm_wpc.csv'
    where_clause = 'Path=='+'"NYIS-PJM"'
    header_row=['ATC','Start','Stop','Calculator','Path','Product','Calc_Time','Limiting FG','Dfax','ResImp','C10','C11','C12','C13','C14']
    data_type_inspection = 100 #number of rows to inspect to determine data type.  Default=100.  Set to 0 for all rows.
    date_fmt='%d/%m/%Y %H:%M:%S'
    csv_out_name = r'C:\temp\out.csv'
    write_mode='w'  # 'w'=write (overwrite), 'a'=append
    query_result = select(csv_in_name, where_clause, header_row\
                            ,data_type_inspection,\
                            date_fmt,csv_out_name)
    if csv_out_name=='':
        for i in range(len(query_result)):
            print query_result[i]
    else:
        print 'saved to file: ', csv_out_name
        print '1st 3 rows: '
        print query_result[0:3]

        # open in default app
        cmdln=''

        # open in notepad
        #cmdln='notepad.exe'

        # open in notepad++
        #cmdln=r'C:\Users\advena\AppData\Local\Microsoft\AppV\Client\Integration\EFCD14B3-B8C3-479E-B3D6-355F883AC278\Root\Notepad++\notepad++.exe'

        #open
        if ' ' in cmdln: cmdln = '"' + cmdln + '"'
        if ' ' in csv_out_name and csv_out_name[0]!='"':
            cmdln += '"' + csv_out_name + '"'
        else:
            cmdln = (cmdln + ' ' + csv_out_name).strip()
        os.startfile(cmdln)


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


