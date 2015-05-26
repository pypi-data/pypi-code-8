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
                         'retrieve': 'retrieve_output',
                         'output': 'update_output',
                         'simulation': 'simulation_log',
                         'execution': 'execution_log',
                         'status': 'simulation_status',
                         'spawning': 'machine_spawning_time',
}

args_names_dictionary = {
                         'create_task': ['app_type', 'input_file', 'hgs_version', 'debug'],
                         'delete_task': [],
                         'retrieve_output': [],
                         'update_output': ['output_file'],
                         'update_simulation_log': ['log'],
                         'update_execution_log': ['log'],
                         'update_execution_status': ['status'],
                         'update_machine_spawning_time': ['time'],
}

#TODO: add warnings about extra parameters

def createMessage(task, task_name, interface='eth0', **kwargs):
    if task in task_names_dictionary:
        msg_type = task_names_dictionary[task]
    else:
        print "Unexpected task: %s. List of available tasks: %s" % (task, task_names_dictionary.keys())
        raise BaseException
    
    args = args_names_dictionary[msg_type]
    
    for element in args:
        if element not in kwargs.keys():
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
    sender_address = auxiliary.getIPAdreess(interface)
    
    message = {
               'msg_type': msg_type,
               'task_name': task_name,
               'sender_address': sender_address,
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
                    self.callback(message)
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