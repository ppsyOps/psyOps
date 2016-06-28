# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 08:12:19 2016
@author: advena

'''
List of functions:
  sort_unique(list): returns sorted list with no dupes
  quick_unique(list): returns list with no dupes
  quicker_unique(list): elimiates dupes IN PLACE
  cheap_sort: sorts list IN PLACE
  quick_sort: returns sorted list
  dupes: returns pairs of list items and count of ocurrences

  list_examples(): demos the functions in this module
"""

# ----------------------------------------------------------------------------    
#  Function definitions
# ----------------------------------------------------------------------------    

def sort_unique(seq):
    return quick_sort(quick_unique(seq))
    
def quick_unique(seq):
    ### Filter to unique list maintaining order
    ### Fast optioin 
    ### Why assign seen.add to seen_add instead of just calling seen.add? Python 
    ### is a dynamic language, and resolving seen.add each iteration is more 
    ### costly than resolving a local variable. seen.add could have changed 
    ### between iterations, and the runtime isn't smart enough to rule that out. 
    ### To play it safe, it has to check the object each time.    
    ### See also: https://www.peterbe.com/plog/uniqifiers-benchmark
    if len(seq)>0:
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    else:
        return seq

def quicker_unique(seq):
    # More than 2x faster than list_unique(), above but
    # does NOT preserve order
    if len(seq)>0:
        return {}.fromkeys(seq).keys()
    else:
        return seq

def cheap_sort(array):
    # quick sort IN PLACE function, which uses less memory.
    # source: http://rosettacode.org/wiki/Sorting_algorithms/quick_sort#Python
    #
    _cheap_sort(array, 0, len(array) - 1)
 
def _cheap_sort(array, start, stop):
    if stop - start > 0:
        pivot, left, right = array[start], start, stop
        while left <= right:
            while array[left] < pivot:
                left += 1
            while array[right] > pivot:
                right -= 1
            if left <= right:
                array[left], array[right] = array[right], array[left]
                left += 1
                right -= 1
        _cheap_sort(array, start, right)
        _cheap_sort(array, left, stop)
        
def quick_sort(inlist):
    ''' 
    quick_sort is a sorting option that can be used as an
    alternative to the built in list method .sort().
    '''
    if inlist == []: 
        return []
    else:
        pivot = inlist[0]
        lesser = quick_sort([x for x in inlist[1:] if x < pivot])
        greater = quick_sort([x for x in inlist[1:] if x >= pivot])
        return lesser + [pivot] + greater

def dupes(lst, preserve_order=True):
    ret=[]
    #try:
    #    lst = list[lst]
    #except Exception, e:
    #    print('psy_list.counts() error.  ' + str(e))
    #    return 
    if preserve_order:
        unq = quick_unique(lst)
    else:
        unq = set(lst)
    for item in unq:
        ret += [[item, lst.count(item)]]
    return ret

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

# ----------------------------------------------------------------------------    
#  Example us of functions in this module (and some builtins)
# ----------------------------------------------------------------------------    

def list_examples():
    mylist = [9,4,8,9,4,21,45,8,0,7,3,32,6,-45,776,3]
    print(mylist)
    print('')
    print('count duplicates with dupes():')
    print(dupes(mylist))
    print('')
    print('eliminate duplicates with quick_unique():')
    print(quick_unique(mylist))
    print('')
    print('eliminate duplicates with quicker_unique():')
    print(quicker_unique(mylist))
    print('')
    print('eliminate duplicates and sort with sort_unique():')
    print(sort_unique(mylist))
    print('')
    print('sorted in place with builtin .sort(): ' )
    print(sort_unique(mylist))
    print('')
    print('sort with quick_sort: ' )
    print(quick_sort(mylist))
    print('')
    print('sort IN PLACE with cheap_sort: ' )
    print(cheap_sort(mylist))
    print('')
    print('sorted in place with builtin .sort(): ' )
    mylist.sort()

def min_list_2d(list_in, compare_col, ret_col):
    from operator import itemgetter
    return min((e for e in list_in if e[compare_col]), \
               key = itemgetter(1))[ret_col]

def max_list_2d(list_in, compare_col, ret_col):
    from operator import itemgetter
    return max((e for e in list_in if e[compare_col]), \
               key = itemgetter(1))[ret_col]
    
def minmax_list_2d_test():
    mylist =  [['someid-1', None, 4] ,['someid-2', 4545.474, 5] ,['someid-3', 200.1515, 0], \
               ['someid-4', None, None] ,['someid-4', 0, 11]]    
    #mylist =  [['someid-1', None] ,['someid-2', 4545.474] ,['someid-3', 200.1515] , \
    #           ['someid-4', None] ,['someid-4', 0]]
    print min_list_2d(mylist, 1, 0)
    print max_list_2d(mylist, 1, 0)

def compare_2d_lists(list1, list2):
    import pandas as pd
    list2['isin'] = 'x'
    ret_df = pd.merge(list1, list2, how='outer', on=['lists'])
    ret_df = ret_df[ret_df['isin'].isnull()]
    ret_df = ret_df.drop('isin',1)
    return ret_df.tolist()

def list1_not_in_list2(list1, list2): 
    return [x for x in list1 if not x in list2]
# ----------------------------------------------------------------------------    
#  Testing
# ----------------------------------------------------------------------------    

# need to add testing for this module
#list_examples()