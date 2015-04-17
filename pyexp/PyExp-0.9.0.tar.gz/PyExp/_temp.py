import os
import re


core_function_files = [
	"/Users/akomissarov/Dropbox/workspace/PySatDNA/core_functions/annotation_functional.py",
	]

template = "value = raw_inpit(%(request)s) or %(default)s"

def create_config_file(core_function_files):
    """
    """
    for file_name in core_function_files:
        with open(file_name) as fh:
            content = fh.read()
            items = set(re.findall("(project\[[^\s\,\)\(\.]+)", content))
            for item in items:
                data = {
                	
                }
                values = re.findall("\[[\"\']+(\S+?)[\"\']+\]", item)
                print item, values

create_config_file(core_function_files)