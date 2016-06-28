'''
Functions:
    type_fixer: auto convert the input object to a python data type. Works 
                recursivley through lists and tuples.  Great function for
                strings or lists of strings parsed from files.
    
    extract_floats: pareses discreet real numbers (type = float) out of a 
                    single string or a list of strings.

    extract_pos_ints: pareses discreet strings out of a single string.    
    extract_digits: parses and concatenates digits from a string.  Optionally,
                    converts from string to integer.
    extract_num: inferior function to extract floats but with more options
                 (input parameters).
    is_str: implements isinstance(object, str) or isinstance(object, str)
            depending on python version, so your code is compatible with all 
            version of python 2 and 3.     
'''

def type_fixer(obj_in, date_fmts=['%m/%d/%Y', '%m/%d/%y', \
                                    '%m/%d/%Y %H:%M', '%m/%d/%y %H:%M', \
                                    '%m/%d/%Y %H:%M:%S', '%m/%d/%y %H:%M:%S', \
                                    '%Y-%m-%d %H:%M'], \
                 from_string=False, return_list=True):
    ''' 
    Attempts to auto convert each item from a list to native python data type.
    Performs recursively, that is, it will continue through sub-lists.
    
    Returns a list.
    
    Input Paramters:
        obj_in: can be str, datetime, int, float, list or tuple
        date_fmts: a list of date formats you expect.
                   If date format is unknown, submit an empty list.  
                   If an empty list is given, then dateutil.parser parse
                   is used to automatically attempt to find a date format.  
                   Beware that using dateutil.parser will be expensive and
                   could convert some values to date that were not intended
                   to be dates.
        from_string: set to True to force the list items (excluding sub-lists
                     and tuples) to be set to str(list item).strip() before 
                     attempting to set type.  This is useful if you are
                     setting types for a list of parsed string data.
        return_list: always return a list of values, even if the input was 
                     not a list.  This saves you some code if you might
                     need to loop through results.
    '''
    import datetime
    from dateutil.parser import parse
    
    # if needed, convert fmts to a list
    if date_fmts == None or len(date_fmts) == 0:
        date_fmts = []
    elif isinstance(date_fmts, list):
        'skip ahead'    
    elif isinstance(date_fmts, tuple):
        date_fmts=list(date_fmts)    
    elif isinstance(date_fmts, int) or \
          isinstance(date_fmts, float) or \
          isinstance(date_fmts, datetime.datetime):
        date_fmts=[date_fmts]
    else:
        try:
            # python 2
            if isinstance(date_fmts, basestring):
                date_fmts=[date_fmts]
        except:
            # python 3
            if isinstance(date_fmts, str):
                date_fmts=[date_fmts]
    
    ret = []    
    obj_type = type(obj_in)
    if isinstance(obj_in, list):
        'do nothing'
    elif isinstance(obj_in, tuple):
        obj_in = list(obj_in)
    else:
        obj_in = [obj_in]
    
    #  begin converting data types
    for item in obj_in:
        if isinstance(item, tuple): #convert tuple to list before continuing
            item = list[item]
        if isinstance(item, list):  # recurse if item is a list
            ret += [type_fixer(item)]
        else:
            if from_string:
                try:
                    item=str(item).strip()
                except:
                    "Cannot convert item to string.  That's odd."
            try:
                ret += [int(item)]
            except:
                try:
                    ret += [float(item)]
                except:
                        typed = False
                        if len(date_fmts) == 0:  # auto-detect date format
                            try: 
                                ret += [parse(item)]
                                typed = True
                            except:
                                typed = False
                        else:
                            for fmt in date_fmts:
                                try:
                                    ret += [datetime.datetime.strptime(item,fmt)]
                                    typed = True
                                    break
                                except:
                                    typed = False
                        if not typed:
                            ret += [item]
    
    # If object was not a list or tuple, extract the object from the list and return it.
    if not return_list and not (obj_type == list or obj_type == tuple):
            return ret[0]
    else:
        return ret

def extract_floats(strings_in):
    '''
    Pareses discreet strings out of a single string or a list of strings.
    Returns LIST of float(s)

    strings_in: can be a string or list of strings
    '''
    from re import findall
    
    if type(strings_in, list):
        'already a list'
    elif type(strings_in, tuple):
        strings_in = list(tuple) # tuple to list
    else:
        strings_in = [str(strings_in)]  #string to list of string
    
    for str in strings_in:
        return findall("[-+]?\d+[\.]?\d*", strings_in)


def extract_pos_ints(str_in):
    [int(s) for s in str_in.split() if s.isdigit()]

    
def extract_digits(str_in, to_int=False):
    '''
    extracts all digits found in str_in and concatenates to a single string
    
    Parameters:
        str_in: input string from which to extract digits
        to_int: attempt to convert result to python integer (type int)
    '''
    ret = ""
    for chr in str_in:
        if chr.isdigit():
            ret += chr
    if to_int: 
        try:
            return int(ret)
        except:
            return 0
    else:
        return ret

def extract_num(str_in, quick=False, spec_chars='+-.', to_num=True, no_digit=0):
    '''
    Extracts digits and special charaters (+, -, .)  from a string and converts
    the string to a number (float or int)
    
    Returns    
    
    Parameters
        str_in: string input from which to extract number
        quick: if true, don't try hard, only finds digits, 
               and don't convert to numeric data type
        spec_chars: look for these special characters in addition to digits.
                    for + or -: only kept if before first digit
                    for ".": only keeps first ocurrence
        to_num: if true, try to convert the result to an integer or float.
                if false, return string.
        no_digit (0 or None): return this value if no digits are found in  
                              str_in
    '''

    str_in = str(str_in) # just in case input was not a string
    ret = "" # Build return value.  Start with empty string

    if quick or len(spec_chars) == 0:    
        # keep only digits
        for chr in str_in:
            if chr.isdigit():
                ret += chr
    else:
        # keep only digits and special characters
        for chr in str_in or chr in spec_chars:
            if chr.isdigit():
                ret += chr
    
    if not quick:        
        # remove all but the first decimal point
        if '.' in ret:
            dec = ret.index('.')  #dec = position of first decimal point in string  
            ret = ret[:dec].replace('.','') + '.' + ret[dec+1:].replace('.','')
        #ret = ret[::-1]  #reverse the order of characters
        #ret = ret.replace('.','',ret.count('.')-1) #remove the last (which as the first) decimal point)
        #ret = ret[::-1] # return character order to original
    
        # remove +/- signs not at begining of number
        while "+" in ret[1:]:
            ret = ret[0] + ret[1:].replace("+","")
        while "-" in ret[1:]:
            ret = ret[0] + ret[1:].replace("+","")
    
        # attempt to convert to integer or float if possible.
        if to_num == 'float':
            ret=float(ret)
        elif to_num == 'int':
            ret=int(ret)
        if to_num:
            try:
                ret=int(ret)
            except:
                try:
                    ret=float(ret)
                except:
                    ret=no_digit
    if ret == '':
        return no_digit
    else:
        return ret

    
def is_str(obj_in):
    try:  
        # Python 2.7+, 3+ compliant
        return isinstance(obj_in, str)
    except:  
        # Python 2.7- compliant
        return isinstance(obj_in, basestring)


def to_datetime(obj_in, date_fmts=['%m/%d/%Y', '%m/%d/%y', \
                                    '%m/%d/%Y %H:%M', '%m/%d/%y %H:%M', \
                                    '%m/%d/%Y %H:%M:%S', '%m/%d/%y %H:%M:%S', \
                                    '%Y-%m-%d %H:%M']):

    import datetime

    if isinstance(obj_in, datetime.datetime):
        return obj_in

    # if needed, convert fmts to a list
    if date_fmts == None or len(date_fmts) == 0:
        date_fmts = []
    elif isinstance(date_fmts, list) or isinstance(date_fmts, tuple):
        'skip ahead'    
    else:
        try:
            # python 2
            if isinstance(date_fmts, basestring):
                date_fmts=[date_fmts]
        except:
            # python 3
            if isinstance(date_fmts, str):
                date_fmts=[date_fmts]

    if len(date_fmts) == 0:  # auto-detect date format
        #try: 
        from dateutil.parser import parse
        return parse(obj_in)
        #except:
        return
    else:
        for fmt in date_fmts:
            try:
                return datetime.datetime.strptime(obj_in,fmt)
            except:
                ' do nothing '
