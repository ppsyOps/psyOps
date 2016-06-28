# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 18:53:09 2016

@author: advena

These simple regex functions are meant more as examples than true functions.  
in most cases, it is more useful to use the contents of the function as a 
recipe than is to execute the function. Of course, the choice is yours.
"""

import re

def serch_vs_match():
    print ('''
    search vs match.
    Search finds the first occurrene anywhere in the string.  You will use: if search in search_in:
    match looks only at the begining of the string.''')

def search(search_for, search_in):
    '''
    Looks for search_for anywhere in search_in
    returns True or False
    parameters;
        search_for: the text to find
        search_in: the string being searched
    '''
    #create the regex formated search string    
    re_str = search_for
    regex = re.compile(search_for)
    if regex in search_in:
        return True
    else:
        return False

def search_group(re_str, search_in, group_num=None):
    '''
    adapted from http://www.tutorialspoint.com/python/python_reg_expressions.htm
    re_str: a regex string with one or many search items, like: r'(.*) are (.*?) .*'
    searh_in: the string in which to search, like: "Cats are smarter than dogs";
    group_nums: re.search.group(num) takes a number.  group_nums is a python
                list of num values
    ''' 
    re_search = re.search(re_str, search_in, re.M|re.I)
    if group_num == None:
        ret = re_search.group()
    else:
        ret = re_search.group(group_num)
    return ret

def starts_with(searh_for, search_in):
    '''
    Looks for search_for anywhere in search_in
    returns True or False
    parameters;
        search_for: the text to find
        search_in: the string being searched
    '''
    #create the regex formated search string    
    match_str = search_for
    if re.match(searh_for, search_in, re.M|re.I):
        return True
    else:
        return False

def match_help():
    '''
    The match Function
This function attempts to match RE pattern to string with optional flags.

Here is the syntax for this function −

re.match(pattern, string, flags=0)
Here is the description of the parameters:

Parameter	Description
pattern	This is the regular expression to be matched.
string	This is the string, which would be searched to match the pattern at 
          the beginning of string.
flags	You can specify different flags using bitwise OR (|). These are 
          modifiers, which are listed in the table below.

The re.match function returns a match object on success, None on failure. 
We usegroup(num) or groups() function of match object to get matched expression.

Match Object Methods   Description
group(num=0)	        This method returns entire match (or specific subgroup num)
groups()       	   This method returns all matching subgroups in a tuple 
                       (empty if there weren't any)

Example
#!/usr/bin/python
import re

line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)

if matchObj:
   print "matchObj.group() : ", matchObj.group()
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2)
else:
   print "No match!!"
When the above code is executed, it produces following result −

matchObj.group() :  Cats are smarter than dogs
matchObj.group(1) :  Cats
matchObj.group(2) :  smarter
    
    '''


def replace(find_str, repl_str, find_in_str, max=0):
    '''
    find_str: regex string/pattern to find
    repl_str: replace found text with this text
    find_in: the string in which you are searching
    max: max number of replacements to make.  
         0 indicates no max.
    '''
    return re.sub(find_str, repl_str, find_in_str, max)


def re_modifiers_help():
    print(''' 
    example function dmeonstrating regex modifiers.
    from http://www.tutorialspoint.com/python/python_reg_expressions.htm    
    
    Example re.match('a','ABC', re.I)"
    returns true because:
        match looks at the beginning of the string
        re.I means search case insensitive
        'a' is the begining of 'ABC', is searchin
         case insensitive as per modifier re.I.
    
    re.I  = case insensitive
    re.L  = locale: impacts \W and \W as well as
    re.M  = case insensitive
    re.S  = case insensitive
    re.U  = case insensitive
    re.X  = case insensitive
    re.  = case insensitive
    ''')
    
def re_control_chars_help():
    print('''
    Except for control characters, all characters
    match themslef in regex.  you can escape a 
    control character by preceding it with a backslash (\)
    from http://www.tutorialspoint.com/python/python_reg_expressions.htm    

Control Characters
    ^ = begin of line")
    $ = end of line")
    [..] = match any character in brackets")
     = ")
    [^..] = match any character NOT in brackets")
    re* = 0+ matches of preceding expression")
    re+ = 1+ matches of preceding expression")
    re? = 0 to 1 matches of preceding expression")
    re{n} = exaclty n matches of preceding")
    re{n,} = n+ matches of preceding")
    re{n,m} = n to m matches of preceding")
    a|b = match a or b")
    (re) = groups regex and remembers matched expressions")
    ?-imx = temp toggle ON i, m or x options within regex.")
    "      If in parentheses, only that area is affected.)
    ?imx = temp toggle OFF i, m or x options within regex.")
    "      If in parentheses, only that area is affected.)
    ?: re = groups regex w/o remembering matched espressions")
    :ixm: re = temp toggle on i, m or x otpions within parens")
    :ixm: re = temp toggle OFF i, m or x otpions within parens")
    ?#... = comment")
    ?= re = sepcify position using patter.  doesn't have range.")
    ?! re = specify pattern using negation.  Doesn't have a range.")
    ?> re = match independen pattern w/o backtracking")
    \w = match word chars")
    \W = match nonword chars")
    \s = match whitepsace equiv (\t\n\r\f)")
    \S = match nonwhitepace")
    \d = match digits.  equivalent to [0-9]")
    \D = match nondigits")
    \A = matches begining of string")
    \Z = matches end of string.  if newline exists, matches just before newlinw")
    \z = matches end of string")
    \G = matches where last match finished")
    \b = matches word boundaries when outside brackers. ")
         matches backspace (0x08) when inside brackets.")
    \B = matches nonword boundaries.")
    \n, \t, etc. = matches newlines, carriage returns, tabs, etc.")
    \1...\9 = matches nth grouped subexpression")
    \10 = matches nth grouped subexpression if it matched already.")
          Otherwise, refers to the octal representaiton of a character code.")
   
Examples
    python  match 'python'
    [Pp]ython match python or Python
    rub[ye] match ruby or rube
    [aeiou] match lowercase vowel
    [0-9] match any digit; same as [0123456789]
    [a-z] match lowercase ascii letter
    [A-Z] match uppercase ascii letter
    [a-zA-Z0-9]  match any of the above (any letter or digit
    [^aeiou] match anything but lowercase vowel
    [^0-9] match any non-digit
    
Special Characters
    .     match any character bu newline
    \d    digit
    \D    non-digit
    \s    whitepace
    \w    sinle word character: [A-Za-z0-9_]
    \W    single NONword character: [^A-Za-z0-9_]

Repetition Cases
    ruby?    'rub' or 'ruby'; y is optional
    ruby*    'rub' plus 0+ ys
    ruby+    'rub' plus 1+ ys
    \d{3}    exactly 3 digits
    \d{3,}   3 or more digits
    \d{3,5}  3 to 5 digits

Nongreedy repetition
    matches smalles number of repetitions
    <.*>    greedy repetition: matches "<python>perl>"
    <.*?>    nongreedy repetition: matches "<python>" in "<python>perl>"

Grouping with Parentheses
    \D\d+    no gorup: + repeats \d
    (\D\d)+  grouped:  + repeats \D\d pair
    ([Pp]ython(,)?)+  match "Python", "Python, python, python", etc.
    (['"])[^\1]*\1    single or double-quoted string.
                      \1 matches whatever the 1st group matched
                      \2 matches whatever the 2nd group matched, etc.

Alternatives
    python|perl    'pyhton' or 'perl'
    rub(y|le)      ruby or ruble
    Python(!+|\?)  'Python' followed by one or more ! or one ?
    
Anchors
    ^Python    'Python' at the beginning of the string or line  
    Python$    'Python' at the end of the string or line
    \APython   'Python' at the beginning of the string 
    Python\Z   'Python' at the end of the string 
    \bPython\b 'Python' at a word boundary
    \BPython\B 'Python' NOT at a word boundary
    \brub\B    match word beginning with rub like rub or ruby, not scrub
    Python(?=!) match 'Python', if followed by and exclamation point.
    Python(?!!) match 'Python', if NOT followed by and exclamation point.
    R(?#comment) match 'R'; the rest is a comment
    R(?i)uby    match capital 'R', case insensitive 'uby'
    rub(?:y|le) Group only w/o createing \1 backreference


    ''')
