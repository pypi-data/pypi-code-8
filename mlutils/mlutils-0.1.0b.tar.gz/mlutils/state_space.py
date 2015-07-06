#!/usr/bin/python

""" Routines to generate, manipulate and search state space.
 
    State space should be describe as a dictionary or list of any iteratable type, e.g. list, tuple or string. 
    Each element of space description shold enumirate all posible values of correcponding attribute.  
    Examples: 
        {"name" : ("John", "Mary"), "status" : ("busy", "available")}
        {"name" : ["John", "Mary"], "status" : ["busy", "available"]}
        [("John", "Mary"), ("busy", "available")]

    State could be represented as a dictionary or list of attribute values.  Attribute values could be any type or None.
    Example: {"name" : "John", "status" : "busy" } 
             ["John", "busy"]
   
"""
import copy
import collections
import nary_tree
from mtools import *


def generate_full_state_space(space_desc):
    """ Function generate all possible states in state space. State space descriptor is accepted in the form of dictinary or list. 
        States are generated accordingly in form of dictionary or list
        If not-iterable type is part of state space description 
        it will be transferer to all generated states as is. You can use this to pass reference on certain data to all states. 
    """
    
    space_size = len(space_desc)
    if isinstance(space_desc,list):
        attr_list = range(space_size)
        next_state = [0]*space_size
    elif isinstance(space_desc, dict):
        attr_list = space_desc.keys()
        next_state = {}
    else:
        assert 0, "Incorrect type of space descriptor, expected list or dict"

    # build internal representation
    space_desc_in = []
    attr_list_in = []
    for attr in attr_list:
        if isinstance(space_desc[attr], collections.Iterable) and len(space_desc[attr]) > 0 :
            space_desc_in.append(space_desc[attr])
            attr_list_in.append(attr) 
        else:
            next_state[attr] = space_desc[attr]
            
    # combine attributes              
    space_in_size = len(space_desc_in)            
    for vals in combine_values(space_desc_in):           
        for i in range(space_in_size):
            next_state[attr_list_in[i]] = vals[i]
        yield copy.deepcopy(next_state)


def generate_distance_states(space_desc, initial_state, distance, verbose = 0):
    """ Function generate all states reachable from given initial state by changing certain number of attributes 
        geven by parameter distance. If distance is a list, function will iterate over it.
        State space descriptor is accepted in the form of dictinary or list. Inital state should be represented by identical type.
        Size of initial state should match size of state space description 
        Note: using dictionary for space_desc/initial_state involve additional memory overhead to make internal list representation
    """
    assert isinstance(space_desc,list) == isinstance(initial_state,list), "Type of space descriptor mismatch type of initial state"
    assert len(space_desc) == len(initial_state), "Length of space descriptor is not equal to length of initial state"       
        
    space_size = len(space_desc)
    if isinstance(space_desc,list):
        attr_list = range(space_size)
        next_state = [0]*space_size
    elif isinstance(space_desc, dict):
        attr_list = space_desc.keys()
        next_state = {}
    else:
        assert 0, "Incorrect type of space descriptor, expected list or dict"
    
    # build internal representation
    space_desc_in = []
    initial_state_in = []
    attr_list_in = []
    for attr in attr_list:
        if isinstance(space_desc[attr], collections.Iterable) and len(space_desc[attr]) > 0 :
            space_desc_in.append(space_desc[attr])
            initial_state_in.append(initial_state[attr])
            attr_list_in.append(attr) 
        else:
            next_state[attr] = space_desc[attr]         
            
    if isinstance(distance, int ):
        distance_in = [distance]
    else:
        distance_in = distance
       
    # generate indexes for subset of attributes
    space_in_size = len(space_desc_in)         
    for dist in distance_in: 
        for attr_in_idx in binomial_subset(space_in_size, dist):    
            if verbose: print "attr subset: ", attr_in_idx
            attr_in_vals = []
            for idx in attr_in_idx:
                vals = []
                # build list of values to combine
                for val in space_desc_in[idx]:
                    if val != initial_state_in[idx]:
                        vals.append(val)
                attr_in_vals.append(vals)
            if verbose: print "values to combine: ", attr_in_vals
            
            # set next state
            for i in range(space_in_size):
                next_state[attr_list_in[i]] = initial_state_in[i]
                           
            # combine selected attributes      
            for vals in combine_values(attr_in_vals):           
                for i in range(len(attr_in_idx)):
                    next_state[attr_list_in[attr_in_idx[i]]] = vals[i]
                yield copy.deepcopy(next_state)    
            
            

def build_state_space_depth_first(initial_state, state_gen_func, goal_test_func, max_depth):
    """ Build state space tree based on generator function state_gen_func(state)
        Return tuple (top node with initial state, node with goal state or None )
    """
    top = nary_tree.NAryTreeNode(initial_state)
    if goal_test_func(initial_state):
        return (top, top)
    else:
        if max_depth > 0 :
            for state in state_gen_func(initial_state):
                (node, goal) = build_state_space_depth_first(state, state_gen_func, goal_test_func, max_depth-1)
                top.add(node)
                if goal != None:
                    return (top, goal)        
        return (top, None)

def build_state_space_breadth_first(initial_state, state_gen_func, goal_test_func, max_depth):
    """ Build state space tree based on generator function state_gen_func(state)
        Return tuple (top node with initial state, node with goal state or None )
    """
    top = nary_tree.NAryTreeNode(initial_state)
    if goal_test_func(initial_state):
        return (top, top)
    else:
        cur_level = [top]
        while max_depth > 0:
            next_level = []
            for cur_node in cur_level:
                for state in state_gen_func(cur_node.data):
                    node = cur_node.add(state)
                    next_level.append(node)
                    if goal_test_func(state) :
                        return (top, node)
            max_depth = max_depth - 1
            cur_level = next_level        
        return (top, None)


test_enabled = {"full_space_generator" : 1, 
                "distance_states" : 1 }
      
if __name__ == '__main__':
    space_desc_list = [ [11, 12], (21, 22, 23), "5678", None]
    initial_state_list = [11, 22, "8", None]
    space_desc_dict = {"A1":(11,12,13), "B2":[21,22,23], "R": "345"}
    initial_state_dict = {"A1":11, "B2": 22, "R": None }
    
    if test_enabled["full_space_generator"]:
        print "Test of generate_full_state_space() - list"
        for state in generate_full_state_space(space_desc_list):  
            print state
    
        print "Test of generate_full_state_space() - dict"
        for state in generate_full_state_space(space_desc_dict):  
            if state["A1"] == 11: state["Tag"] = "A1 = 11"            
            print state

        
    if test_enabled["distance_states"]:
        print "Test of generate_distance_states() - list"
        for state in generate_distance_states(space_desc_list, initial_state_list, 2, 1): 
            print state                    
    
        print "Test of generate_distance_states() - dict"
        for state in generate_distance_states(space_desc_dict, initial_state_dict, 2, 1): 
            print state   
    
        