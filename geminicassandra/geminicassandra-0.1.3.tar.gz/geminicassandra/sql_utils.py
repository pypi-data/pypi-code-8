"""
these are utilities to parse and transform SQL statements
"""

import re
import sys


def get_select_cols_and_rest(query):
    """
    Separate the a list of selected columns from
    the rest of the query

    Returns:
        1. a list of the selected columns
        2. a string of the rest of the query after the SELECT
    """
    from_loc = query.lower().find("from")

    raw_select_clause = query[0:from_loc].rstrip()
    rest_of_query = query[from_loc:len(query)]

    # remove the SELECT keyword from the query
    select_pattern = re.compile("select", re.IGNORECASE)
    raw_select_clause = select_pattern.sub('', raw_select_clause)

    # now create and iterate through a list of of the SELECT'ed columns
    selected_columns = raw_select_clause.split(',')
    selected_columns = [c.strip() for c in selected_columns]

    return selected_columns, rest_of_query

def get_query_parts(query):
    """
    Extract the where clause of this CQL query.
    """
    
    select_loc = query.lower().find('select')
    from_loc = query.lower().find('from')
    
    if from_loc == -1:
        sys.exit("ERROR: query must contain FROM <table>")
    
    from_end = len(query)
    
    where_loc = query.lower().find("where")
    
    if where_loc > -1:
        from_end = where_loc
    
    where_end = len(query)
    
    for keyword in ["order by", "limit", "allow_filtering"]:
        stop = query.find(keyword)
        if stop > -1:
            from_end = min(stop, from_end)
            where_end = min(stop, where_end)
        
    where_clause = ""
    rest = ""
    from_table = query[from_loc + 4: from_end].strip()
    select_clause = query[select_loc:from_loc]
    
    # remove the SELECT keyword from the query
    select_pattern = re.compile("select", re.IGNORECASE)
    select_clause = select_pattern.sub('', select_clause)

    # now create and iterate through a list of of the SELECT'ed columns
    selected_columns = select_clause.split(',')
    selected_columns = [c.strip() for c in selected_columns]
    
    if where_loc > -1:
        where_clause = query[where_loc + 5: where_end].strip()
    if where_end < len(query):
        rest = query[where_end:].strip()
    
    return selected_columns, from_table, where_clause, rest   

def ensure_columns(query, cols):
    """
    if a query is missing any of these list of columns, add them
    and return the new query string
    """
    sel_cols, rest = get_select_cols_and_rest(query)
    sel_cols = [x.lower() for x in sel_cols]
    for c in cols:
        c = c.lower()
        if c not in sel_cols:
            sel_cols += [c]

    sel_string = ", ".join(sel_cols)
    return "select {sel_string} {rest}".format(**locals())
