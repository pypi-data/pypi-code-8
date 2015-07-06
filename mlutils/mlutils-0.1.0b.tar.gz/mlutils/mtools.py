#!/usr/bin/python
""" Miscellaneous math tools 
"""

def binomial_subset(n,k):
    """ Function generate indexes for k-size subsets from n-size set, 
        e.g. for n=3, k=2 it will generate sequence [0,1], [0,2], [1,2]    
    """
    idx = range(k)
    j = 0
    while k-j > 0:
        if k-1-j < k-1:
            if idx[k-1-j] < idx[k-j]-1:
                idx[k-1-j] += 1  
                while k-j < k:
                    idx[k-j] = idx[k-1-j] + 1
                    j -= 1
            else:
                j += 1
        else: 
            while idx[k-1] < n:
                yield idx
                idx[k-1] += 1
            j += 1

def combine_values(vals_list):
    """ Function generate all possible combinations of values in given list, 
        e.g. vals_list  [[1,2], [3,4]] 
        it will generate sequence [1,3], [1,4], [2,3], [2,4]        
    """
    attr_num = len(vals_list)
    idx = [0]*attr_num
    vals = [0]*attr_num
    vals_len = [0]*attr_num
    for i in range(attr_num):
        vals_len[i] = len(vals_list[i])
        
    while 1:       
        for i in range(attr_num): 
            vals[i] = vals_list[i][idx[i]]  
        yield vals
        
        j = 0
        while idx[j] == vals_len[j]-1:
            idx[j] = 0
            j += 1        
            if j > attr_num - 1: return        
        else:
            idx[j] += 1 
                     
                     
def factorial(n):
    f = 1
    for i in range(2, n+1):
        f = f * i
    return f


if __name__ == '__main__':
    
    print "Binomial subsets of 2 from 4 : "
    for subset in binomial_subset(4,2): 
        print subset
    print "Combinations: "
    for vals in combine_values([(1,2,3), ('A', 'B')]): 
        print vals
    print "Factorial of 3 = ", factorial(3)

