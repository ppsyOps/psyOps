'''

Pandas I/O: http://pandas.pydata.org/pandas-docs/stable/io.html

'''

def csv_to_df(file_name, header):
    ''' This is a simple example function.  Use of a fucntion is overkill.  Just copy and use the code.		
		Parameters:
		    file_name - a file-like object
			sep = delimiter such as ',' for comma, '\+s'  for space, or a regular expression.
			header= row number containing header; header=None for no header,
			names = column_headers like ['col1', 'col2']
			more parameters: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
	'''
	import pandas as pd
    df = pd.read_csv(file_name,
        header=1)

def df_to_csv(file_name):	
    import pandas as pd	
	try:
	    with open(file_name, 'a+') as f:
	        df.to_csv(f, index=False, header=True)
		return 0
	except ErrorValue, e:
	    print('Unable to export dataframe to file' + file_name)
	    return e

def dict_to_csv(dict_in, file_name, mode='a'):
    '''
    Exports contents of a python dictionary into a csv file.
    http://code.activestate.com/lists/python-tutor/104332/
    # https://docs.python.org/2/library/csv.html
    # class csv.DictWriter(csvfile, fieldnames, restval='', extrasaction='raise', dialect='excel', *args, **kwds)
    # Create an object which operates like a regular writer but maps dictionaries onto output rows. The fieldnames parameter is a sequence of keys that identify the order in which values in the dictionary passed to the writerow() method are written to the csvfile. The optional restval parameter specifies the value to be written if the dictionary is missing a key in fieldnames. If the dictionary passed to the writerow() method contains a key not found in fieldnames, the optional extrasaction parameter indicates what action to take. If it is set to 'raise' a ValueError is raised. If it is set to 'ignore', extra values in the dictionary are ignored. Any other optional or keyword arguments are passed to the underlying writer instance.
    # Note that unlike the DictReader class, the fieldnames parameter of the DictWriter is not optional. Since Python’s dict objects are not ordered, there is not enough information available to deduce the order in which the row should be written to the csvfile.
    # A short usage example:
    
    import csv
    with open('names.csv', 'w') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    
    '''
    
'''
    import csv
    import sys
    with open(file_name, mode) as csvfile:
        writer = csv.writer(sys.stdout)
        writer.writerows(dict_in.items())    
'''    