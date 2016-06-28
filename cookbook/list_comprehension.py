'''
 Guido van Rossum prefers list comprehensions to constructs using map, filter, reduce and lambda.
 list comprehension should ever so slightly faster, because it does not require a python
 function call.  

[ <output value>  for <element> in <list>  <optional criteria>  ]
'''
# filter num_list to only values less than 5.
[ num for num in num_list if num < 5 ]


#create a list of numbers 1 to 100
[i for i in irange(100)]
## returns [1,2,3,4, ... ,100]

#create a list of squares of 1 to 100
[i*i for i in irange(100)]
## returns [1,4,9,16,25. .. ,100]

# create a list (of Pythagorean triples)
[(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2]
## returns:[(3, 4, 5), (5, 12, 13), (6, 8, 10), (7, 24, 25), (8, 15, 17), (9, 12, 15), (10, 24, 26), (12, 16, 20), (15, 20, 25), (20, 21, 29)]

# change every item in a list
>>> lst = ['a  ','  b','  c   ']
>>> lst
['a  ','  b','  c   ']
>>> lst =[item.strip(' ') for item in lst]
>>> lst
['a','b','c']

# filter a list
>>> lst = ['a','b','c','aa','bb','cde']
>>> lst
['a', 'b', 'c', 'aa', 'bb', 'cde']
>>> lst2 = [s for s in lst if 'c' in s]
>>> lst2
['c', 'cde']

# filter and modify at the same time
>>> lst = ['a','b','c']
>>> lst
['a', 'b', 'c']
>>> lst2 = ['<<'+str(item)+'>>' for item in lst if item=='a']
>>> lst2
['<<a>>']


[[s.strip(' ') for s in item.split('=')] for item in lst if ('=' in item and '#' not in item)]
