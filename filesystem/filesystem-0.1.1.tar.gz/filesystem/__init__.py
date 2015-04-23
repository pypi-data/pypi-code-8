import glob as glob_lib
import os

__version__ = "0.1.1"

def get_facts(pathname):
    head, tail = os.path.split(pathname)
    result = {}
    result["modified"] = os.path.getmtime(pathname)
    result["created"] = os.path.getctime(pathname)
    result["access"] = os.path.getatime(pathname)
    result["name"] = tail
    result["size"] = os.path.getsize(pathname)
    result["abspath"] = os.path.abspath(pathname)
    result["dirname"] = os.path.dirname(pathname)
    result["is_dir"] = os.path.isdir(pathname)
    result["is_file"] = os.path.isfile(pathname)
    result["is_link"] = os.path.islink(pathname)
    result["ext"] = tail.split(".")[-1] if result["is_file"] else ""
    return result

def glob(path):
    result = []
    for x in glob_lib.glob(path):
        result.append(get_facts(x))
    return result

def walk(path):
    results = []
    for root, dirs, files in os.walk(path):
        results.append(get_facts(root))
        results.extend([get_facts(os.path.join(root,x)) for x in files])
    return results

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

