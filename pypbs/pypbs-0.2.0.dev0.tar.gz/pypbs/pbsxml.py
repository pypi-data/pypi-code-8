import re

def parse_xml(xmltree, index_tag):
    '''
    Parse -x xml output for various commands

    :param xml.etree.ElementTree.Element xmltree: etree xml from pbsnodes -x
    :param str index_tag: tag to index dictionary elements by
    :return: dict of {index_tag: {attr1:val,}}
    '''
    nodes = {}
    for node in xmltree:
        tdict = parse_sub_xml(node)
        if 'jobs' in tdict and isinstance(tdict['jobs'],str):
            tdict['jobs'] = [tdict['jobs']]
        if index_tag:
            nodes[tdict[index_tag]] = tdict
    return nodes

def parse_sub_xml(xmltree):
    '''
    Return dictionary for xml tree
    '''
    tdict = {}
    for attrib in xmltree:
        text = attrib.text
        if text:
            text = attrib.text.strip()
        if not text:
            tdict[attrib.tag] = parse_sub_xml(attrib)
        elif attrib.tag == 'jobs':
            tdict[attrib.tag] = parse_job_list(text)
        elif '/' in text:
            # Don't mess with things that have '/' in them
            tdict[attrib.tag] = text
        else:
            tdict[attrib.tag] = parse_list_string(text)
    return tdict

def parse_list_string(string):
    '''
    Parse out any list like string that is separated by comma
    If individual list items have key=value, convert to dict
    If there are no commas then just return original string

    :param str string: list like string
    :return: list or dict depending on input string
    '''
    # Splits on comma if word or equal sign on the left and word on the right
    parts = re.split('(?<=[\w\)=]),(?=\w)',string)
    # Return original string
    if len(parts) == 1:
        return string

    # No sub dictionary required
    if '=' not in string:
        return parts

    _dict = {}
    for i in range(len(parts)):
        part = parts[i]
        # No subdict
        if '(' not in part and ')' not in part:
            k,v = part.split('=')
            if not v:
                v = None
            _dict[k] = v

    # Now do another search for subdict patterns
    subdict = {}
    p = '(\w+)=([\w\d\.]+\(.*?\)(?: \S+\(.*?\)){0,})'
    stuff = re.findall(p, string)
    for key, values in stuff:
        subdict[key] = {}
        defs = re.findall('(?:(\S+)\((.*?)\))', values)
        for _key, d in defs:
            subdict[key][_key] = parse_list_string(d)
    _dict.update(subdict)
    return _dict

def parse_job_list(joblist):
    '''
    Parses a joblist

    :param str joblist: string of jobs
    :return: list of separated jobs
    '''
    jobs = re.split('(?<=[a-zA-Z]),(?=\d)', joblist)
    return list(filter(lambda x: x != '', jobs))
