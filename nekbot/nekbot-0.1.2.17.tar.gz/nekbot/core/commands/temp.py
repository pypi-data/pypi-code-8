# coding=utf-8
from Queue import Queue
from collections import defaultdict
import re
import threading
import datetime
from nekbot.core.exceptions import PrintableException

__author__ = 'nekmo'

class CancelTemp: pass

class TempTimeout(PrintableException):
    pass

class TempRegexList(defaultdict):
    def __init__(self):
        defaultdict.__init__(self, list)
        self.delete_timer = None
        # comandos ordenados por tiempo para ser eliminados en su momento
        self.to_delete = defaultdict(list)

    def start_delete_timer(self):
        if self.delete_timer is not None:
            self.delete_timer.cancel()
        timers = sorted(self.to_delete.keys())
        if not timers: return
        timer = timers[0]
        t = (timer - datetime.datetime.now()).seconds
        if t < 0: t = 0
        self.delete_timer = threading.Timer(t, self.start_deletion, (timer,))
        self.delete_timer.start()

    def start_deletion(self, timer):
        temp_regex_list = self.to_delete[timer]
        for temp_regex in temp_regex_list:
            self.delete(temp_regex, TempTimeout('Timeout: exceeded %i seconds' % temp_regex.timeout))
        if timer in self:
            del self.to_delete[timer]
        self.start_delete_timer()

    def register(self, temp_regex):
        # Registrando por su tiempo para eliminación para borrarlo si supera el tiempo
        self.to_delete[temp_regex.delete_t].append(temp_regex)
        # Registrando por su pattern para poder hacer el match fácilmente
        self[temp_regex.pattern].append(temp_regex)
        # Se reinicia el tiempo para el próximo borrado
        self.start_delete_timer()

    def delete(self, temp_regex, msg=None):
        if msg is None: msg = CancelTemp
        temp_regex.write(msg)
        t = temp_regex.delete_t
        reload_timer = False
        if t in self.to_delete and temp_regex in self.to_delete[t]:
            self.to_delete[t].remove(temp_regex)
            if not self.to_delete[t]:
                # No hay más para esta hora. Se borra el listado.
                del self.to_delete[t]
                reload_timer = True
        if temp_regex.pattern in self and temp_regex in self[temp_regex.pattern]:
            self[temp_regex.pattern].remove(temp_regex)
            if not self[temp_regex.pattern]:
                # No hay más para esta hora. Se borra el listado.
                del self[temp_regex.pattern]
                reload_timer = True
            if not self.to_delete[temp_regex.delete_t]:
                # No hay más para esta hora. Se borra el listado.
                del self.to_delete[temp_regex.delete_t]
                reload_timer = True
        if reload_timer:
            # Ha habido un cambio en la línea cronológica. Volver a iniciar timer
            self.start_delete_timer()

    def match_message(self, msg):
        for pattern, temp_regex_list in self.items():
            if not pattern.match(msg.body): continue
            match = re.findall(pattern, msg.body)
            for temp_regex in temp_regex_list:
                new_msg = msg.copy()
                new_msg.match = match
                temp_regex.write(new_msg)

temp_regex_patterns = TempRegexList()

class TempRegex(object):
    def __init__(self, protocol, pattern, user=None, timeout=300, no_raise=False):
        if isinstance(pattern, (str, unicode)):
            pattern = re.compile(pattern)
        self.no_raise = no_raise
        self.pattern = pattern
        self.protocol = protocol
        self.user = user
        self.timeout = timeout
        self.delete_t = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.queue = Queue()
        # Registrar este nuevo TempRegex
        temp_regex_patterns.register(self)

    def write(self, msg):
        self.queue.put(msg)

    def read(self):
        while self.delete_t > datetime.datetime.now():
            msg = self.queue.get()
            if isinstance(msg, CancelTemp):
                break
            if isinstance(msg, Exception):
                if self.no_raise:
                    yield msg
                else:
                    raise msg
            yield msg
        yield CancelTemp

    def done(self):
        temp_regex_patterns.delete(self)