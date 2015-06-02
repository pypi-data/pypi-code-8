# This is a simple adaptor to generate a state_collection from a directory of autosaves

import funtool.adaptor

import funtool.state_collection
import funtool.state
import funtool.group
import funtool.grouping_selector

import gzip
import json
import zipfile
import codecs
import chardet

import os


# If it is a users_directory it is assumed that each folder is a user and each subfolder is a project
# Both users_directory and projects_directory assume that groups should be created, if you need just the states use collection_directory 
# All subfolders in a collection_directory will be importeted, as will all the sub-project folders for a users or projects directory

# Adaptor Functions
     
def import_users_directory(adaptor,state_collection, overriding_parameters=None,loggers=None):
    adaptor_parameters= funtool.adaptor.get_adaptor_parameters(adaptor, overriding_parameters)
    return _import_users_directory(adaptor_parameters.get('data_location'),{})

def import_projects_directory(adaptor,state_collection, overriding_parameters=None,loggers=None):
    adaptor_parameters= funtool.adaptor.get_adaptor_parameters(adaptor, overriding_parameters)
    return _import_projects_directory(adaptor_parameters.get('data_location'),{})

def import_directory(adaptor,state_collection, overriding_parameters=None,loggers=None):
    adaptor_parameters= funtool.adaptor.get_adaptor_parameters(adaptor, overriding_parameters)
    return _import_collection_directory(adaptor_parameters.get('data_location'),{})






# Internal Functions

def _import_collection_directory(directory_path, meta):
    return funtool.state_collection.StateCollection(states=_import_directory(directory_path,meta),groupings={})
    

def _import_projects_directory(directory_path, meta):
    project_directories= [ project_directory for project_directory in os.listdir(directory_path) 
                            if os.path.isdir(os.path.join(directory_path,project_directory))]
    state_list=[]
    groups={}
    for project_directory in project_directories:
        project_meta = meta.copy()
        project_meta.update({'project_directory':project_directory}) 
        project_states = _import_directory( os.path.join(directory_path, project_directory), project_meta )
        project_group = funtool.group.create_group('projects_directory',project_states,{}, project_meta, {})
        groups[project_directory]=project_group
        state_list += project_states

    return funtool.state_collection.StateCollection(states=state_list,groupings={'projects_directory':groups}) 

def _import_users_directory(directory_path, meta):
    user_directories= [ user_directory for user_directory in os.listdir(directory_path) 
                            if os.path.isdir(os.path.join(directory_path,user_directory))]
    state_collection = funtool.state_collection.StateCollection([],{})
    for user_directory in user_directories:
        user_meta=meta.copy()
        user_meta.update({'user_directory':user_directory})
        projects_collection= _import_projects_directory( os.path.join(directory_path,user_directory), user_meta )
        user_group= funtool.group.create_group('users_directory',projects_collection.states,{}, user_meta, {})
        state_collection= funtool.state_collection.join_state_collections( 
            state_collection, 
            projects_collection
        )
        state_collection= funtool.state_collection.add_group_to_grouping(state_collection,'users_directory',user_group, user_directory)
    return state_collection
       

def _import_directory(directory_path, meta):
    state_list = []
    for (directory_path,subdirectories,files) in os.walk(directory_path):
        for f in files:
            extension= os.path.splitext(f)[1][1:].lower()
            state_meta = meta.copy()
            state_meta.update({'filename':f, 'directory':directory_path})
            if extension == 'json':
                state_list.append(create_state_from_json( os.path.join( directory_path,f), None, state_meta )) 
            elif extension == 'gz':
                state_list.append(create_state_from_gz( os.path.join( directory_path,f), None, state_meta )) 
            elif extension == 'sb2':
                state_list.append(create_state_from_sb2( os.path.join( directory_path,f), None, state_meta )) 
    return state_list
 

def create_state_from_json(file_location, state_id, meta ):
    try:
        with open(file_location, 'rb') as f:
            data = json.loads(str(f.read(), 'utf-8'))
            new_state = funtool.state.State(id=state_id, data={'json':data},measures={},meta=meta,groupings={})
    except (ValueError, UnicodeDecodeError):
        encoding= _detect_encoding(file_location)
        print(encoding)
        with open(file_location, 'rb') as f:
            data = json.loads(str(f.read(), encoding))
            new_state = funtool.state.State(id=state_id, data={'json':data},measures={},meta=meta,groupings={})
    return new_state

def create_state_from_gz(file_location, state_id, meta ):
    with gzip.open(file_location) as f:
        data = json.loads(str(f.read(),'utf-8'))
        new_state = funtool.state.State(id=state_id, data={'json':data},measures={},meta=meta,groupings={})
    return new_state

def create_state_from_sb2(file_location, state_id, meta ):
    archive = zipfile.ZipFile(file_location, 'r')
    sb2_json = archive.read('project.json')
    data = json.loads(str(sb2_json,'utf-8'))
    new_state = funtool.state.State(id=state_id, data={'json':data},measures={},meta=meta,groupings={})
    return new_state


def _detect_encoding(file_location):
    test_bytes = min(32, os.path.getsize(file_location))
    with open(file_location, 'rb') as f:
        raw= f.read(test_bytes)

        if raw.startswith(codecs.BOM_UTF8):
            encoding = 'utf-8-sig'
        else:
            result = chardet.detect(raw)
            encoding = result['encoding']
    return encoding
    
