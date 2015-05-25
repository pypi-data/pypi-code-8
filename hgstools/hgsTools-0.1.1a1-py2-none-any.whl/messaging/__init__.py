'''
Created on May 25, 2015

@author: andrei
'''

from kombu import Connection
import time
from Queue import Empty

import logging
import netifaces as ni

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

def getIPAdreess(interface='eth0'):
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return addr

def createMessage(task, task_name, interface='eth0', **kwargs):
    if task in task_names_dictionary:
        msg_type = task_names_dictionary[task]
    else:
        print "Unexpected task: %s. List of available tasks: %s" % (task, task_names_dictionary.keys())
        raise
    
    sender_address = getIPAdreess(interface)
    
    message = {
               'msg_type': msg_type,
               'task_name': task_name,
               'sender_address': sender_address,
               'kwargs': kwargs,
    }
    
    return message


class MessageConsumer(object):
    def __init__(self, connectionLink, queueName, callback, logFileName='MessageConsumer.log'):
        self.queueName = queueName
        self.connectionLink = connectionLink
        self.callback = callback
        
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler('/var/tmp/' + logFileName)
        hdlr.setFormatter(formatter)
        
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.DEBUG)

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
    
    def constantConsume(self):
        while True:
            if not self.consumeOneMsg():
                time.sleep(1)


class MessageProducer(object):
    def __init__(self, connectionLink, queueName, logFileName='MessageProducer.log'):
        self.queueName = queueName
        self.connectionLink = connectionLink
        
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler('/var/tmp/' + logFileName)
        hdlr.setFormatter(formatter)
        
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.DEBUG)
        
    def publish(self, message):
        with Connection(self.connectionLink) as conn:
            with conn.SimpleQueue(self.queueName) as queue:
                queue.put(message)