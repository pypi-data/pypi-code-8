try:
    import unittest2 as unittest
except:
    import unittest

def make_node_info(**kwargs):
    return {
        'name': kwargs.get('name','foo'),
        'np': kwargs.get('np','10'),
        'status': {
            'ncpus': kwargs.get('ncpus','10'),
            'loadave': kwargs.get('loadave','0.0')
            },
            'jobs': kwargs.get('jobs',[])
    }

def make_job_info(**kwargs):
    return {
        'Job_Id': kwargs.get('Job_Id','foo'),
        'exec_host': kwargs.get('exec_host','host.example.com/0,2-4')
    }
