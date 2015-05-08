import jarvis.utils.redisconnect as redisconnect
from jarvis.commands import debug, debug_dir
import json
import weakref

class RClient(object):
    def __init__(self, store_prefix):
        self.store_prefix = store_prefix                
        self.notif_channel = redisconnect.connect().pubsub()
        self.notif_channel.psubscribe(self.get_channel_prefix() + ":*")
        self.update_channel = redisconnect.connect()
        self.subscriptions = {} # subscriptions contains weak references to RClientObjects

    def id_join(self, *args):
        """Create an id from several parts."""
        return ":".join(args)
    
    def get_key(self, key):
        """Build a redis key from an object key."""
        return self.id_join(self.store_prefix, key)

    def get_channel_prefix(self):
        """Return the pubsub channel prefix."""
        return self.store_prefix
        
    def get_channel_id(self, key):
        """Build a pubsub channel name from an object key."""
        return self.id_join(self.get_channel_prefix(), key)
    
    def subscribe(self, obj):
        """Subscribe."""
        key = self.get_key(obj.key())
        if key not in self.subscriptions:
            obj.statedump()
            self.subscriptions = weakref.ref(obj)
        else:
            return self.subscriptions[key]()

    def register_op(self, script):
        return self.update_channel.register_script(script)
            
    def run(self, script, *args, **kwargs):
        return script(*args, **kwargs)

    def read_event(self):
        for e in self.notif_channel.listen():
            return e

    def interrupt(self):
        self.stop = True
    
    def events(self):
        while not self.stop:
            ret = self.read_event()
            if ret:
                yield ret

class RClientObjectOperation(object):
    def __init__(self, o):
        self.object = object
        
    def apply(self, operation):
        pass
                        
class RClientObject(object):
    def __init__(self, client, key):
        self.client = client
        self.key_ = key
        state_dump_script = self.get_state_dump()
        debug(state_dump_script)
        self.__class__.STATE_DUMP_SCRIPT = self.client.register_op(state_dump_script)
        self.client.subscribe(self)
        self.init_ops()

    def init_ops(self):
        clazz = self.__class__
#        if hasattr(clazz, "ops"):
#            return
        debug("coucou")
        clazz.ops = {}
        op_class_name_prefix = clazz.__name__ + "Operation"
        globs = globals()
        for op_class_name, op in globs.iteritems():
            if op_class_name.startswith(op_class_name_prefix) and issubclass(op, RClientObjectOperation):
                op_name = op_class_name[len(op_class_name_prefix):].lower()
                clazz.ops[op_name] = globs[op_class_name]
    
    def key(self):
        return self.key_

    def typeString(self):
        return self.__class__.__name__[7:].lower()
    
    def get_channel_id(self):
        return self.typeString() + ":" + self.key()

    def get_state_dump(self):
        return self.STATE_DUMP % (self.client.get_channel_prefix(), self.typeString())
    
    def statedump(self):
        """Send a message to the store to dump completely the state into a message on subscription channel
           To be overridden in sub classes"""
        self.client.run(self.__class__.STATE_DUMP_SCRIPT, [self.client.get_channel_prefix(), self.key()])
        s = self.client.read_event()
        debug(s)
        s = self.client.read_event()
        data = s['data']
        debug("data=", data)        
        j = json.loads(data)["value"]        
        debug(unicode(j).encode("utf-8"))

    def op_apply(self, op_name, operation):
        self.ops[op_name].apply(operation)

