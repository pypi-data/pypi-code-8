# Copyright 2011 OpenStack Foundation
# Copyright 2013 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy
import json
import threading
import time

from six import moves

import oslo_messaging
from oslo_messaging._drivers import base


class FakeIncomingMessage(base.IncomingMessage):
    def __init__(self, listener, ctxt, message, reply_q, requeue):
        super(FakeIncomingMessage, self).__init__(listener, ctxt, message)
        self.requeue_callback = requeue
        self._reply_q = reply_q

    def reply(self, reply=None, failure=None, log_failure=True):
        if self._reply_q:
            failure = failure[1] if failure else None
            self._reply_q.put((reply, failure))

    def requeue(self):
        self.requeue_callback()


class FakeListener(base.Listener):

    def __init__(self, driver, exchange_manager, targets, pool=None):
        super(FakeListener, self).__init__(driver)
        self._exchange_manager = exchange_manager
        self._targets = targets
        self._pool = pool
        self._stopped = threading.Event()

        # NOTE(sileht): Ensure that all needed queues exists even the listener
        # have not been polled yet
        for target in self._targets:
            exchange = self._exchange_manager.get_exchange(target.exchange)
            exchange.ensure_queue(target, pool)

    def poll(self, timeout=None):
        if timeout is not None:
            deadline = time.time() + timeout
        else:
            deadline = None
        while not self._stopped.is_set():
            for target in self._targets:
                exchange = self._exchange_manager.get_exchange(target.exchange)
                (ctxt, message, reply_q, requeue) = exchange.poll(target,
                                                                  self._pool)
                if message is not None:
                    message = FakeIncomingMessage(self, ctxt, message,
                                                  reply_q, requeue)
                    return message
            if deadline is not None:
                pause = deadline - time.time()
                if pause < 0:
                    break
                pause = min(pause, 0.050)
            else:
                pause = 0.050
            time.sleep(pause)
        return None

    def stop(self):
        self._stopped.set()


class FakeExchange(object):

    def __init__(self, name):
        self.name = name
        self._queues_lock = threading.RLock()
        self._topic_queues = {}
        self._server_queues = {}

    def ensure_queue(self, target, pool):
        with self._queues_lock:
            if target.server:
                self._get_server_queue(target.topic, target.server)
            else:
                self._get_topic_queue(target.topic, pool)

    def _get_topic_queue(self, topic, pool=None):
        if pool and (topic, pool) not in self._topic_queues:
            # NOTE(sileht): if the pool name is set, we need to
            # copy all the already delivered messages from the
            # default queue to this queue
            self._topic_queues[(topic, pool)] = copy.deepcopy(
                self._get_topic_queue(topic))
        return self._topic_queues.setdefault((topic, pool), [])

    def _get_server_queue(self, topic, server):
        return self._server_queues.setdefault((topic, server), [])

    def deliver_message(self, topic, ctxt, message,
                        server=None, fanout=False, reply_q=None):
        with self._queues_lock:
            if fanout:
                queues = [q for t, q in self._server_queues.items()
                          if t[0] == topic]
            elif server is not None:
                queues = [self._get_server_queue(topic, server)]
            else:
                # NOTE(sileht): ensure at least the queue without
                # pool name exists
                self._get_topic_queue(topic)
                queues = [q for t, q in self._topic_queues.items()
                          if t[0] == topic]

            def requeue():
                self.deliver_message(topic, ctxt, message, server=server,
                                     fanout=fanout, reply_q=reply_q)

            for queue in queues:
                queue.append((ctxt, message, reply_q, requeue))

    def poll(self, target, pool):
        with self._queues_lock:
            if target.server:
                queue = self._get_server_queue(target.topic, target.server)
            else:
                queue = self._get_topic_queue(target.topic, pool)
            return queue.pop(0) if queue else (None, None, None, None)


class FakeExchangeManager(object):
    def __init__(self, default_exchange):
        self._default_exchange = default_exchange
        self._exchanges_lock = threading.Lock()
        self._exchanges = {}

    def get_exchange(self, name):
        if name is None:
            name = self._default_exchange
        with self._exchanges_lock:
            return self._exchanges.setdefault(name, FakeExchange(name))


class FakeDriver(base.BaseDriver):

    def __init__(self, conf, url, default_exchange=None,
                 allowed_remote_exmods=None):
        super(FakeDriver, self).__init__(conf, url, default_exchange,
                                         allowed_remote_exmods)

        self._exchange_manager = FakeExchangeManager(default_exchange)

    def require_features(self, requeue=True):
        pass

    @staticmethod
    def _check_serialize(message):
        """Make sure a message intended for rpc can be serialized.

        We specifically want to use json, not our own jsonutils because
        jsonutils has some extra logic to automatically convert objects to
        primitive types so that they can be serialized.  We want to catch all
        cases where non-primitive types make it into this code and treat it as
        an error.
        """
        json.dumps(message)

    def _send(self, target, ctxt, message, wait_for_reply=None, timeout=None):
        self._check_serialize(message)

        exchange = self._exchange_manager.get_exchange(target.exchange)

        reply_q = None
        if wait_for_reply:
            reply_q = moves.queue.Queue()

        exchange.deliver_message(target.topic, ctxt, message,
                                 server=target.server,
                                 fanout=target.fanout,
                                 reply_q=reply_q)

        if wait_for_reply:
            try:
                reply, failure = reply_q.get(timeout=timeout)
                if failure:
                    raise failure
                else:
                    return reply
            except moves.queue.Empty:
                raise oslo_messaging.MessagingTimeout(
                    'No reply on topic %s' % target.topic)

        return None

    def send(self, target, ctxt, message, wait_for_reply=None, timeout=None,
             retry=None):
        # NOTE(sileht): retry doesn't need to be implemented, the fake
        # transport always works
        return self._send(target, ctxt, message, wait_for_reply, timeout)

    def send_notification(self, target, ctxt, message, version, retry=None):
        # NOTE(sileht): retry doesn't need to be implemented, the fake
        # transport always works
        self._send(target, ctxt, message)

    def listen(self, target):
        exchange = target.exchange or self._default_exchange
        listener = FakeListener(self, self._exchange_manager,
                                [oslo_messaging.Target(
                                    topic=target.topic,
                                    server=target.server,
                                    exchange=exchange),
                                 oslo_messaging.Target(
                                     topic=target.topic,
                                     exchange=exchange)])
        return listener

    def listen_for_notifications(self, targets_and_priorities, pool):
        targets = [
            oslo_messaging.Target(
                topic='%s.%s' % (target.topic, priority),
                exchange=target.exchange)
            for target, priority in targets_and_priorities]
        listener = FakeListener(self, self._exchange_manager, targets, pool)

        return listener

    def cleanup(self):
        pass
