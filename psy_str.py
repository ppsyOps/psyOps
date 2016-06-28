'''
strpy.py is a string toolset.
 
Functions:
    space_cleaner: replace all multiple adjacent spaces with a single space.
    space_split: parse a string based on spaces.  Multiple spaces are treated
                 the same as a single space.
	strip2(): extension strip() that can be run on strings or lists
			  and has options for applying strip only to part of 
			  a string.
	in_list(value): finds the first occurnce of value in a list
'''

def space_cleaner(str_in):
    '''
    Replaces multiple adjacent spaces with a single space.
    Returns a string.
    '''
    temp = str(str_in).strip()
    while '  ' in temp:
        temp = temp.replace('  ', ' ')
    return temp 

def space_split(str_in):
    '''
    Parses a string based on spaces.  Multiple spaces are treated
           the same as a single space.
    Returns a list.
    '''
    temp = str(str_in).strip()
    while '  ' in temp:
        temp = temp.replace('  ', ' ')
    return temp.split(' ')


def in_list(list_item, list_in):
	''' A fast way to find the first (and only 1st) item of a list.
			string_in is any string value.
		Returns index of first occurence of value.  
			If not found, returns None.
		list_in: python list to be searched
		list_item: entry/item to find in the list 
	'''
	try:
	    return list_in.index(list_item)
	except ValueError:
	    return None
	#Else:
	#    "Do something with variable value"

#def filter_list(list_in, value)
#   #This function is for example only.  Just use the single line of code.
#   return = [x for x in list_in if x == value]
	
def strip2(string_in, chars=", ", string_part='lr'):
	'''
	Clean_str is like {string expresssion}.strip() extended.  Originally designed 
		to cleanup "dirty" strings retrieved from csv files.

	Returns: a string with the left, right and/or middle of the string stippped
			of specific characters.  

			
	Parameters:
		string in (required): the string to be cleaned.
		chars (optional): a string of individual characters to be 
						filtered found and stripped out.
		string_part (optional):
				  'l': trim from left (beginning) of string.
				  'r': trim from right (end) of string
				 'lr': trim both ends.
				  'a': clean all, left, right and middle of string
				 'n:': clean only from character position n, where n is an integer
				 ':m': clean only from character position m, where m is an integer
				'n:m': clean only from character postion n to m (pythonic), 
				       where n is an integer
	Examples:  
			>>> clean_str(' """"  abc"')
			'abc'
			>>> clean_str('asdf jkl; qwerty',[" jk"],["a"])
			'asdfl; qwerty'
			>>> clean_str([1,"23","345"],["3"],["a"])
			[1,"2","45"]
			>>> clean_str([1,"23","345"],["3"],["r"])
			[1,"2","345"]
			>>> clean_str([1,"23","345"],["3"],["1:2"])
			[1,"2","345"]
	'''
	try: 
		chars = str(chars)
		string_part = str(string_part).lower()
	except:
		return string_in
	if isinstance(string_in, list) or isinstance(string_in, tuple):
		try:
			ret=[]
			for i in range(len(string_in)):
				ret[i] += [strip2(string_in[i])]
			return ret
		except:
			return string_in
	else:
		try: 
			ret = str(string_in)
		except:
			return string_in
		try:
			if string_part == 'lr' or string_part == 'lr':
				return string_in.strip(chars)
			elif string_part == 'l':
				return string_in.lstrip(chars)
			elif string_part == 'r':
				return string_in.rstrip(chars)
			elif ':' in string_part:
				nm = string_part.split(':')
				try: n=int(nm[0])
				except: n=0
				try: m=int(nm[1])
				except: m=len(string_in)
				return string_in[:n] + string_in[n:m].strip(chars) + string_in[m:]
		except:
			return string_in
	
	
