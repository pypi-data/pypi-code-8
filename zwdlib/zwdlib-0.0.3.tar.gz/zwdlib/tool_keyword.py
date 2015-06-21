# encoding: utf-8
'''
Created on 2015年4月1日

@author: Lenovo
'''
from tool_env import replace_spaces


def find(keywords, text, results=[], all=True):
    '''
    >>> a = {'te': {'test': {'test2': {'test2 3': {}}}}, 'another': {}}
    >>> results = []
    >>> find(a, 'test it and test2', results)
    >>> results
    [('te', 2), ('test', 2), ('test2', 1)]
    >>> results = []
    >>> find(a, 'test it and test2   3', results)
    >>> results
    [('te', 2), ('test', 2), ('test2', 1), ('test2 3', 1)]
    >>> results = []
    >>> find(a, 'test it and test2   3 another', results)
    >>> results
    [('te', 2), ('test', 2), ('test2', 1), ('test2 3', 1), ('another', 1)]
    '''
    text = replace_spaces(text)
    for k in keywords.keys():
        c = text.count(k)
        if c:
            results.append((k,c))
            find(keywords.get(k), text, results, False)
            if not all:
                return
        
        
def push(the_dict, word):
    '''
    >>> push(the_dict,'test')
    {'test': {}}
    >>> push(the_dict,'another')
    {'test': {}, 'another': {}}
    >>> push(the_dict,'test2')
    {'test': {'test2': {}}, 'another': {}}
    >>> push(the_dict,'te')
    {'te': {'test': {'test2': {}}}, 'another': {}}
    >>> push(the_dict,'test2 3')
    {'te': {'test': {'test2': {'test2 3': {}}}}, 'another': {}}
    '''
    keys = the_dict.keys()
    for key in keys:
        if key in word:
            push(the_dict.get(key), word)
            return the_dict
        if word in key:
            v = the_dict.pop(key)
#             print "the v", v
            the_dict.setdefault(word, {key: v})
            return the_dict
    
    the_dict.setdefault(word, {})
    
    return the_dict

if __name__ == '__main__':
    import doctest
    the_dict = {}
    print doctest.testmod(verbose=False, report=True)
#     a = {}
#     push(a, 'test')
#     push(a,'another')
#     push(a,'test2')