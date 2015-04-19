import pytest
from src.main import *

test_files = [  "examples/C/filenames/script", "examples/Clojure/index.cljs.hl", "examples/Forth/core.fth", 
                "examples/GAP/Magic.gd", "examples/JavaScript/steelseries-min.js",
                "examples/Matlab/FTLE_reg.m", "examples/Perl6/for.t",
                "examples/VimL/solarized.vim", "examples/C/cpu.c",
                "examples/D/mpq.d", "examples/Go/api.pb.go", 
                "examples/HTML+ERB/index.html.erb"]

number_of_comments = [
    195,    # examples/C/filenames/script
    13,     # examples/Clojure/index.cljs.hl
    0,      # examples/Forth/core.fth
    303,    # examples/GAP/Magic.gd 
    2,      # examples/JavaScript/steelseries-min.js
    0,      # examples/Matlab/FTLE_reg.m
    76,    # examples/Perl6/for.t
    420,   # examples/VimL/solarized.vim
    80,     # examples/C/cpu.c
    36,     # examples/D/mpq.d 
    184,    # examples/Go/api.pb.go
    10      # examples/HTML+ERB/index.html.erb
]

def test_get_comment_tokens():
    from pygments.lexers.c_cpp import CLexer

    file_text_test = "int main(int argc, char[] argv){\n//This is a comment\n}\n"
    c_lexer = CLexer()

    results = []
    for comment in get_comment_tokens(file_text_test, c_lexer):
        results.append(comment)

    assert len(results) == 1
    assert results[0] == "//This is a comment\n"

def test_get_tokens_from_file():
    for index,file in enumerate(test_files, 0):
        result = get_tokens_from_file(file)
        #print(index)
        print(file)
        assert number_of_comments[index] == len(result.keys())

test_A = "// TODO This is a example todo with #TAGS #TODOAWESOME"
     
test_B = "#todo This is a example todo with #TAGS #TODOAWESOME"

test_C = """/**TODO This is a todo 
         #HASHTAGGALORE 
         #TWITTERSUCKS 
         */"""

test_D = """Comments here


         TODO This is a todo
         This is a body #HASHTAGGALORE 
         #TWITTERSUCKS 

         TODO This is a second todo
         #TASKSKSKSK"""

test_E = """/* TODO This is a todo
        *
        * TODO  This is a new todo
        *       With a body too!
        *
        * TODO This is the third one
        *      lets keep it going... #BRICKHACKS
        *
        * TODO And a final lonely one...
        */"""

def test_find_Keywords():
    test_A_findKey = find_Keywords(test_A, ["TODO"])

    assert len(test_A_findKey) == 1

    test_B_findKey = find_Keywords(test_B, ["TODO"])

    assert len(test_B_findKey) == 0

    test_C_findKey = find_Keywords(test_C, ["TODO"])

    assert len(test_C_findKey) == 1

    test_D_findKey = find_Keywords(test_D, ["TODO"])

    assert len(test_D_findKey) == 2

    test_E_findKey = find_Keywords(test_E, ["TODO"])

    assert len(test_E_findKey) == 4

def test_merge_single_line_comments():
    token_to_line_mapping = {}
    token_to_line_mapping[1] = "# Line 1"
    token_to_line_mapping[2] = "# Line 2"
    token_to_line_mapping[3] = "# Line 3"
    token_to_line_mapping[4] = "# Line 4"
    token_to_line_mapping[6] = "# Line 6"
    token_to_line_mapping[7] = "# Line 7"

    merged_result = merge_single_line_comments(token_to_line_mapping)

    # Check that the lines we expect to merge were merged
    assert 1 in merged_result.keys() and 6 in merged_result.keys()


