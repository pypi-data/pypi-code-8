#!/usr/bin/python

import copy
import mlutils.state_space as state_space


def example_1():
    """ mlutils usage example  
    """   
    
    problem_description = """ Problem description: 
        wolf, goat and cabbage should be carried from left side of the rive to right one. 
        
        Restrictions:
        -- Boat can take only one object (wolf or goat or cabbage)  
        -- Wolf can not be left on the same side of the river with goat. 
        -- Goat can not be left on the same side of the rivbuild_state_space_breadth_firster with cabbage    
    """
    
    print problem_description
        
    state_space_desc = {"wolf" : ('L','R'), "goat" : ('L','R'), "cabbage" : ('L','R'), "boat" : ('L','R')}
    initial_state = {"wolf" : 'L', "goat" : 'L', "cabbage" : 'L', "boat" : 'L' }
    goal_state = {"wolf" : 'R', "goat" : 'R', "cabbage" : 'R', "boat" : 'R' }
   
    print "Represent state space as ", state_space_desc
    print "Initial state: ", initial_state
    print "Goal state: ", goal_state
   
    def restiction_func(state_from, state_to):
        """ Return True if transition from <state_from> to <state_to> is valid
            otherwise test_state_space_generatorreturn False
        """
        rc = True
        num = 0
        rc &= state_from["boat"] != state_to["boat"]
        rc &= state_to["wolf"] != state_to["goat"] or state_to["goat"] == state_to["boat"]
        rc &= state_to["goat"] != state_to["cabbage"] or state_to["cabbage"] == state_to["boat"]
        num += state_from["wolf"] != state_to["wolf"]
        num += state_from["goat"] != state_to["goat"]
        num += state_from["cabbage"] != state_to["cabbage"]
        rc &= (num <= 1)
        return rc

    def state_gen_func1(initial_state):
        """ Generate appropriate states based on full state space generation  approach 
            1. build full state space
            2. return valid states based on initial state and restriction function
        """
        full_state_space = []
        if len(full_state_space) == 0 :
            for state in state_space.generate_full_state_space(state_space_desc):
                full_state_space.append(state) 
            
        for state in full_state_space:
            if restiction_func(initial_state, state):
                yield state
                
    def state_gen_func2(initial_state):
        """ Generate appropriate states based on distance state space generation approach 
        """  
        for state in state_space.generate_distance_states(state_space_desc, initial_state, [1,2]):
            if restiction_func(initial_state, state):
                yield state
        
    def test_func(state):
        return state == goal_state
        
        
    print "\nTry depth-first search"   
    (top, goal) = state_space.build_state_space_depth_first(initial_state, state_gen_func1, test_func, 10)
    if goal:    
        print "Goal found at level: ", goal.level()
        goal.print_path()        
    else:
        print "Goal is not found\n", top
    
    print "\nTry breadth-first search"
    (top, goal) = state_space.build_state_space_breadth_first(initial_state, state_gen_func2, test_func, 10)
    if goal:    
        print "Goal found at level: ", goal.level()
        goal.print_path()        
    else:
        print "Goal is not found\n", top
  
    
if __name__ == '__main__':

    example_1()


