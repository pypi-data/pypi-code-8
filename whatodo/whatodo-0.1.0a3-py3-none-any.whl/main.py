import sys
import os
import argparse
import pygments
import json
from argparse import ArgumentParser
from pygments.token import *
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from src.todo import TODO

global_error_list = []

def parse_args():
    '''
    Argument Parsing Helper Function

    Setups and runs the arg parse library to parse the command line arguments for us.

    Returns
    -------
        Already populated set of arguments ready for the taking.
    '''
    app_description = """ WHATODO - 
        Keeps track of your TODO tasks in code. This quick app will scan
        all the files provided and give give you the location and summary 
        of any pending tasks marked with TODO.
    """
    # make the parser
    parser = argparse.ArgumentParser(description = app_description)
    
    # take command line arguments and make array
    parser.add_argument('files', type=str, nargs = '+', help = "File for TODO checking")
    parser.add_argument('-k', '--keywords', type=str, nargs = '*', default=['TODO', 'todo', 'FIXME'], 
                        help = "Keywords for TODO items, case sensitive. Defaults to TODO")
    parser.add_argument('--json', action='store_const', const=True)

    return parser.parse_args()

def get_tokens_from_file(filepath):
    # Read the file in
    file_text = ""

    # Check if filename is an actual valid file
    if os.path.isfile(filepath):
        with open(filepath) as file:
            try:
                for line in file:
                    file_text += line
            except UnicodeDecodeError as e:
                global_error_list.append( filepath + " : " + str(e))
                return {}

    else:
        global_error_list.append("ERROR: " + filepath + " is not a file. Can't process.")
        return {}

    # Determine the lexer we need to use to understand this file
    lexer = None

    # TODO Determine the best way of figuring out the mimetype for certain files,
    #      right now we suck.. Like bad.
    try:
        lexer = guess_lexer_for_filename(filepath, file_text)
    except Exception as e:
        lexer = guess_lexer(file_text)
    finally:
        if lexer == None:
            global_error_list.append("ERROR:\tUnable to find a lexer\n\t\t\tCan't process " + str(filepath))
            return {}
    #print(lexer)
    comments_with_lines = {}

    # Get the comment tokens
    for comment in get_comment_tokens(file_text, lexer):
        for num, line in enumerate(file_text.splitlines(), 1):
            # Eliminate issues with newlines as comments
            if len(comment.strip()) == 0:
                continue
            # Account for multi line comments, only take the comment line
            # since we want to give out where the comment starts
            first_comment_line = comment.splitlines()[0]

            if first_comment_line in line:
                if num in comments_with_lines.keys():
                    continue
                else:
                    comments_with_lines[num] = comment
                    break
    
    return comments_with_lines


def get_comment_tokens(file_text, lexer):
    '''
    Retrieves the set of tokens from the file

    Arguments
    ---------
        file_text : str
            Contains the file text that we are running the lexer through
        lexer : pygments.lexer
            The lexer to use for this file

    Yields
    ------
        comment : str
    '''
    for tokens in pygments.lex(file_text, lexer):
        if tokens[0] in Comment:
            # Just yield the comment string, nothing more
            yield tokens[1]

def find_Keywords(comment, keywords):
    # constants
    array = []
    count = 0

    todos = []

    # loop through key words & split comment into lines
    for keyword in keywords:
        comment_line_by_line = comment.splitlines()

        # loop through the lines and for each word strip white space
        # see if the word in the comment matches keyword
        for index,comment_line in enumerate(comment_line_by_line,0):
            comment_line = comment_line.lstrip()
            index_of_keyword = comment_line.find(keyword)

            # get the index of the matching word 
            # only use if the index is < 10 and > -1
            if index_of_keyword == -1:
                continue
            else:
                if index_of_keyword < 10:
                    rest_of_comment = comment_line_by_line[index:]

                    # loop through remaining comment to locate 
                    # any "empty" lines  
                    found = False
                    for end_index,newLine in enumerate(rest_of_comment,index):
                        if len(newLine) == 0:
                            # if "empty" line found
                            todos.append(comment_line_by_line[index:end_index])
                            found = True
                            break
                    if not found:
                        # if no "empty" lines found 
                        todos.append(rest_of_comment)

                else:
                    continue

    return todos

def merge_single_line_comments(tokens_with_lines):
    '''

    Arguments
    ---------
        tokens_with_lines : dict

    Returns
    -------
        new_token_mapping: dict
            Mapping with the adjecent lines 
    '''
    line_numbers = sorted(tokens_with_lines.keys())

    new_lines_mapping = {}
    new_token_mapping = {}

    # Build a graph mapping to the parent line number
    for line_num in line_numbers:
        new_lines = new_lines_mapping.keys()
        
        # Check for the parent line or a link to it
        if line_num-1 in new_lines:
            old_line = line_num-1
            
            # Follow the mapping to its original
            while(old_line != new_lines_mapping[old_line]):
                old_line = new_lines_mapping[old_line]
            new_lines_mapping[line_num] = old_line
        else:
            # We are a parent, put us on the map!
            new_lines_mapping[line_num] = line_num

    # Now that the graph is built, build the array of comments
    for line_num in line_numbers:
        if line_num != new_lines_mapping[line_num]:
            new_token_mapping[new_lines_mapping[line_num]].append((tokens_with_lines[line_num]))
        else:
            new_token_mapping[line_num] = [tokens_with_lines[line_num]]

    # Merge the comments that are groupped together
    for line_parent in new_token_mapping.keys():
        new_token_mapping[line_parent] = "\n".join(new_token_mapping[line_parent]).strip()

    return new_token_mapping
            
def expand_file_paths(file_names):

    # grab all files and place in list
    final_file_names = []

    # loop through the directories to find files and add them to a list
    for file_name in file_names:

        if os.path.isfile(file_name):
            final_file_names.append(file_name)
        else:
            for dirName, subDirectories, files in os.walk(file_name):
                for f in files:
                    final_file_names.append(os.path.join(dirName, f))
    return final_file_names


def main():
    args = parse_args()

    file_names = expand_file_paths(args.files)
    keywords = args.keywords
    use_json = args.json
    

    #find_Keywords(comment, keywords)
    #comment = "                     #TODO"
    #find_Keywords(comment, keywords)

    TODOS = []
    

    for file in file_names:
        tokens_with_lines = get_tokens_from_file(file)


        cleaned_up_tokens = merge_single_line_comments(tokens_with_lines)
        for line_number in sorted(tokens_with_lines.keys()):
            comment = tokens_with_lines[line_number]
            #print(str(line_number) + " : '" + comment + "'")
            todos = find_Keywords(comment, keywords)

            for todo in todos:
                if len(todo) > 1:
                    todo = "\n".join(todo).strip()
                TODOS.append(TODO(comment, file, line_number, keywords))

    if use_json:
        TODOS_JSON = []
        for t in TODOS:
            TODOS_JSON.append(t.__dict__())
        todos_json = json.dumps(TODOS_JSON)
        print(todos_json)
    else:
        for t in TODOS:
            print(t)
        for error in global_error_list:
            print(error)


if __name__=='__main__':
    main()