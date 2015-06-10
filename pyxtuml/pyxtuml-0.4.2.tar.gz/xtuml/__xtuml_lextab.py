# __xtuml_lextab.py. This file automatically created by PLY (version 3.6). Don't edit!
_tabversion   = '3.5'
_lextokens    = set(['NUMBER', 'PHRASE', 'GUID', 'MINUS', 'INSERT', 'RPAREN', 'SEMICOLON', 'CREATE', 'REF_ID', 'TO', 'COMMA', 'FRACTION', 'ROP', 'TABLE', 'STRING', 'INTO', 'LPAREN', 'ID', 'RELID', 'FROM', 'VALUES', 'CARDINALITY'])
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_comment>\\-\\-([^\\n]*\\n))|(?P<t_COMMA>,)|(?P<t_FRACTION>(\\d+)(\\.\\d+))|(?P<t_RELID>R[0-9]+)|(?P<t_CARDINALITY>(1C))|(?P<t_ID>[A-Za-z_][\\w_]*)|(?P<t_LPAREN>\\()|(?P<t_MINUS>-)|(?P<t_NUMBER>[0-9]+)|(?P<t_RPAREN>\\))|(?P<t_SEMICOLON>;)|(?P<t_STRING>\\\'((\\\'\\\')|[^\\\'])*\\\')|(?P<t_GUID>\\"([^\\\\\\n]|(\\\\.))*?\\")|(?P<t_newline>\\n+)', [None, ('t_comment', 'comment'), None, ('t_COMMA', 'COMMA'), ('t_FRACTION', 'FRACTION'), None, None, ('t_RELID', 'RELID'), ('t_CARDINALITY', 'CARDINALITY'), None, ('t_ID', 'ID'), ('t_LPAREN', 'LPAREN'), ('t_MINUS', 'MINUS'), ('t_NUMBER', 'NUMBER'), ('t_RPAREN', 'RPAREN'), ('t_SEMICOLON', 'SEMICOLON'), ('t_STRING', 'STRING'), None, None, ('t_GUID', 'GUID'), None, None, ('t_newline', 'newline')])]}
_lexstateignore = {'INITIAL': ' \t\r\x0c'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
