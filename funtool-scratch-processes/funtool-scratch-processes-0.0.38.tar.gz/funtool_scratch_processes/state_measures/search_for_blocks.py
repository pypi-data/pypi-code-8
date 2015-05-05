# Functions to look for block patterns inside scratch saves

import funtool.state_measure
import funtool_scratch_processes.state_measures.shared as shared

import funtool_scratch_processes.reporters.to_repl as to_repl




@funtool.state_measure.state_and_parameter_measure
def match_pattern(state, parameters):
    if isinstance(parameters.get('pattern'), list):
        match_count=0
        for script in shared.state_scripts(state):
            stripped_script= shared.strip_position(script)
            if all([ match_condition_item(stripped_script, sub_pattern) for sub_pattern in parameters.get('pattern') ]): #treats the intial list as an and
                match_count+=1
        return match_count
    else:
        raise Exception('match_pattern parameters should be a list')


def match_block( full_script, script_indexes, block_name, block_parameters=None, block_sub=None ):
    """
    Returns True if the block name, parameters, and sub are all in the script
    """
    script= get_subscript( full_script, script_indexes )
    
    if isinstance(script, list) and len(script) > 0:
        if isinstance(script[0],str):   # Check to see if the list describes a block
            if block_name == script[0]:
                match_parameters= False
                if block_parameters is not None:
                    if isinstance(block_parameters, list): 
                        match_parameters= all( [ (len(script) >= i+1) and (script[i+1] == param) for i, param in enumerate(block_parameters) ])
                else:
                    match_parameters= True
                if match_parameters:
                    if block_sub is not None:
                        if match_subblock(full_script, script_indexes, block_sub ):
                            return True
                    else:
                        return True
        for sub_i, subscript in enumerate(script):
            if isinstance(subscript, list):
                if match_block( full_script, script_indexes + [sub_i], block_name, block_parameters, block_sub ):
                    return True
        return False
    else:
        return False


def match_subblock( script, script_indexes, block_sub ):
    block_sub_matches={}
    if 'before' in block_sub:
        block_sub_matches['before']= match_condition( create_before_sublist( script, script_indexes), block_sub['before'] )
    if 'inside' in block_sub:
        block_sub_matches['inside']= match_condition( create_inside_sublist( script, script_indexes), block_sub['inside'] )
    if 'after' in block_sub:
        block_sub_matches['after']= match_condition( create_after_sublist( script, script_indexes), block_sub['after'] )
    return all(block_sub_matches.values())

def match_condition( script, block_conditionals ):
    condition_results=[]
    if isinstance(block_conditionals, list):
        condition_results= [ match_condition_item( script, block_conditional) for block_conditional in block_conditionals ]
    else:
        raise Exception('Must have a list of conditionals to compare to the script. Failed for:\n%s'% str(block_conditionals) )
    return all(condition_results)    

def match_condition_item( script, block_conditional ):
    if isinstance(block_conditional, str):
        return evaluate_str_conditional( script, block_conditional)
    if isinstance(block_conditional, dict):
        return evaluate_dict_conditional( script, block_conditional)
    if isinstance(block_conditional, list):
        return evaluate_list_conditional( script, block_conditional)

def evaluate_str_conditional( script, block_conditional): # For bare block names
    return match_block( script, [], block_conditional)


def evaluate_dict_conditional( script ,block_conditional): # For blocks with parameters or with sub blocks
    if len( block_conditional.keys() ) is 1:
        block_name= next(iter(block_conditional.keys()))
        if isinstance(block_conditional[block_name], dict):
            return match_block( script, [], block_name, block_conditional[block_name].get('parameters'), block_conditonal[block_name].get('sub'))
        else:
            return match_block( script, [], block_name) #if block is not a proper dict then treat it like a bare string
    else:
        raise Exception('Too many blocks specified. Include only one per item.')

def evaluate_list_conditional( script, block_conditional ):
    if isinstance( block_conditional, list) and len(block_conditional) is 1 and isinstance(block_conditional[0], dict) and len( block_conditional[0].keys()) is 1:
        conditional_type= next(iter(block_conditional[0].keys()))
        if (conditional_type in ['with','and']):
            sub_list_results=[]
            for sub_item in block_conditional[0][conditional_type]:
                sub_list_results.append( match_condition_item( script, sub_item ) )
            return all(sub_list_results)
        if conditional_type in ['or_with','or']:
            sub_list_results=[]
            for sub_item in block_conditional[0][conditional_type]:
                sub_list_results.append( match_condition_item( script, sub_item ) )
            return any(sub_list_results)
        if conditional_type in ['not','without']: # not gets distributed across all sub conditional so really a not after an or 
            sub_list_results=[]
            for sub_item in block_conditional[0][conditional_type]:
                sub_list_results.append( match_condition_item( script, sub_item ) )
            return not any(sub_list_results)
    else:
        raise Exception('Only one conditional type can be specified for each list')


def create_before_sublist( script, script_indexes):
    sublist= script[:script_indexes[0]]
    if len(script_index[1:]) > 0:
        sub_part= create_before_sublist(script[script_indexes[0]], script_indexes[1:])
        if len(sub_part) > 0:
            sublist += [ sub_part ]
    return sublist
        
def create_after_sublist( script, script_indexes):
    sublist= script[(script_indexes[0]+1):]
    if len(script_index[1:]) > 0:
        sub_part= create_after_sublist(script[script_indexes[0]], script_indexes[1:])
        if len(sub_part) > 0:
            sublist = [ sub_part ] + sublist
    return sublist

def create_inside_sublist( script, script_indexes):
    sublist= script
    for i in script_indexes:
        sublist= sublist[i]
    return [ item for item in sublist if isinstance(item, list) ]

def get_subscript( script, script_indexes):
    sublist= script
    for i in script_indexes:
        sublist= sublist[i]
    return sublist
    
