# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:43:13 2016

@author: advena
"""

def find_in_list(find_me, list_in, partial=True):
    if partial:
        return filter(lambda s: find_me in s, list_in)
    else:
        return filter(lambda s: find_me == s, list_in)
        
def find_in_list_test():
    list_in = ['apple','orange','grape','grapefruit']
    find_me = 'gra'
    print "Find 'gra' in list_in, where partial=True."
    print "Expected result = ['grape', 'grapefruit']."
    print "Actual result = " 
    print find_in_list(find_me, list_in, partial=True)

    find_me = 'grape'
    print "\n\nFind 'grape' in list_in, where partial=False:"
    print "Expected result = ['grape']."
    print "Actual result = " 
    print find_in_list(find_me, list_in, partial=False)

def test_all():
    find_in_list_test()
