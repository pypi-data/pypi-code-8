'''
Created on May 25, 2015

@author: andrei
'''

from kombu import Connection
import time
from Queue import Empty
from hgsTools import auxiliary

task_names_dictionary = {
                         'create': 'create_app',
                         'delete': 'delete_app',
                         'retrieve': 'retrieve_cli_output',
                         'output': 'update_output',
                         'accepted': 'app_accepted',
                         'info': 'update_info',
                         'status': 'update_app_status',
                         'spawning': 'update_vm_spawning_time',
}

args_names_dictionary = {
                         'create_app': ['tmp_id', 'app_type', 'input', 'output'],
                         'delete_app': ['app_id'],
                         'retrieve_cli_output': ['app_id'],
                         'update_output': ['app_id', 'output'],
                         'app_accepted': ['app_id'],
                         'update_info': ['app_id', 'info_type', 'info'],
                         'update_app_status': ['app_id', 'status'],
                         'update_vm_spawning_time': ['app_id', 'time'],
}

#TODO: add warnings about extra parameters
#TODO: remove sender_address for messages which don't require that parameter (communication between WI and JC)

def createMessage(m_type, interface='eth0', **kwargs):
    if m_type in task_names_dictionary:
        msg_type = task_names_dictionary[m_type]
    else:
        print "Unexpected type: %s. List of available types: %s" % (m_type, task_names_dictionary.keys())
        raise BaseException
    
    if msg_type not in task_names_dictionary.values() or msg_type not in args_names_dictionary:
        print 'Something is wrong with the library'
        raise BaseException
    
    args = args_names_dictionary[msg_type]
    
    for element in args:
        if element not in kwargs.keys():
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
    return_address = auxiliary.getIPAdreess(interface)
    
    message = {
               'msg_type': msg_type,
               'return_address': return_address,
               'kwargs': kwargs,
    }
    
    return message

def messageCheck(message):
    msg_type = message['msg_type']
    kwargs = message['kwargs']
    
    if msg_type not in task_names_dictionary.values() or msg_type not in args_names_dictionary:
        print 'Something is wrong with the library'
        raise BaseException
    
    args = args_names_dictionary[msg_type]
    
    for element in args:
        if element not in kwargs:
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
    return True

class MessageConsumer(object):
    def __init__(self, connectionLink, queueName, callback, logger=None):
        self.queueName = queueName
        self.connectionLink = connectionLink
        self.callback = callback
        self.logger = logger
        
    def consumeOneMsg(self):
        ret = True
        
        with Connection(self.connectionLink) as conn:
            with conn.SimpleQueue(self.queueName) as queue:
                try:
                    message = queue.get_nowait()
                    self.logger.info('Message received')
                    self.callback(message, self.logger)
                    message.ack()
                except Empty:
                    ret = False
                    
        return ret
    
    def constantConsuming(self):
        self.logger.info('Starting constant consuming')
        
        while True:
            if not self.consumeOneMsg():
                time.sleep(1)


#TODO: add logging information
class MessageProducer(object):
    def __init__(self, connectionLink, queueName, logger=None):
        self.queueName = queueName
        self.connectionLink = connectionLink
        self.logger = logger
        
    def publish(self, message):
        with Connection(self.connectionLink) as conn:
            with conn.SimpleQueue(self.queueName) as queue:
                queue.put(message)