'''
Created on 2014-12-17

@author: zhangziteng
'''
import time

class COM_tools(object):
    def get_timestamp(self):
        timestamp=int(time.time()*1000)
        #timestamp=time.gmtime(Unix timestamp)
        return timestamp
    
if __name__ == '__main__':
    tools=COM_tools()
    print tools.get_timestamp()