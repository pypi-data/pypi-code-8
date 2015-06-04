'''
Created on May 25, 2015

@author: andrei
'''

from kombu import Connection
import time
from Queue import Empty
from hgsTools import auxiliary

task_names_dictionary = {
                         'create': 'create_task',
                         'delete': 'delete_task',
                         'retrieve': 'retrieve_cli_output',
                         'output': 'update_output',
                         'accepted': 'task_accepted',
                         'info': 'update_info',
                         'status': 'update_task_status',
                         'spawning': 'update_vm_spawning_time',
}

args_names_dictionary = {
                         'create_task': ['app_type', 'input', 'output'],
                         'delete_task': [],
                         'retrieve_cli_output': [],
                         'update_output': ['output'],
                         'task_accepted': [],
                         'update_info': ['info_type', 'info'],
                         'update_task_status': ['status'],
                         'update_vm_spawning_time': ['time'],
}

#TODO: add warnings about extra parameters
#TODO: remove sender_address for messages which don't require that parameter (communication between WI and JC)

def createMessage(task, app_id, interface='eth0', **kwargs):
    if task in task_names_dictionary:
        msg_type = task_names_dictionary[task]
    else:
        print "Unexpected task: %s. List of available tasks: %s" % (task, task_names_dictionary.keys())
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
               'app_id': app_id,
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