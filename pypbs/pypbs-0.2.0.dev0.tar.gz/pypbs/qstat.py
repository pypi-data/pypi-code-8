from . import util

def get_qstat_xml(jobs=[]):
    '''
    Returns parsed xml tree object for jobs in jobs list

    :param list jobs: list of job identifiers
    :return: xml.etree.ElementTree
    '''
    return util.pbs_xml_command('qstat', *jobs)
