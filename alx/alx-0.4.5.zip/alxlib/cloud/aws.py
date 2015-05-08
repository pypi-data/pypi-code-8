__author__ = 'Alex Gomes'

import boto.sqs
from boto.sqs.message import Message, RawMessage
import os, sys, logging, time, socket, pprint, time, datetime
import alxlib.key
from gettext import gettext as _

logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("boto").setLevel(logging.CRITICAL)

class AWS():

    _msg_key_na = _('Key not available')

    _attr = { "from":
                      {"data_type": "String",
                           "string_value": ""
                      },
                      "from-ip":
                          {"data_type": "String",
                           "string_value": ""
                           },
                      "to":
                          {"data_type": "String",
                           "string_value": "*"
                           },
                      "cmd":
                          {"data_type": "String",
                           "string_value": "ping"
                           },
                      }

    def __init__(self):
        try:
            self.msg_dict={}
            key = alxlib.key.Key()
            if os.path.isfile(key.get_path()):
                sys.path.insert(0, key.get_dir())

                import alxkey

                self.key = alxkey.alxkey_aws
            else:
                raise (AWS._msg_key_na)
        except:
            raise (AWS._msg_key_na)


    #Connection
    def connect_sqs(self):
        try:
             conn = boto.sqs.connect_to_region(self.key["AWS_REGION"],
                                       aws_access_key_id= self.key["AWS_ACCESS_KEY_ID"],
                                       aws_secret_access_key= self.key["AWS_SECRET_ACCESS_KEY"] )

             self.q = conn.create_queue(self.key["AWS_SQS"], self.key["AWS_INVISIBLE"])
             return self.q
        except:
            logging.critical(_("Connection Failure: possibly bad key"))
            return None

    def msg_get_all(self):
        try:

            self.connect_sqs()

            self.q.set_message_class(RawMessage)

            logging.info("Checking queue {0}, {1} message".format(self.key["AWS_SQS"], self.q.count()))

            msgs = self.q.get_messages(num_messages=10, attributes="All", message_attributes=['.*'])

            if len(msgs) == 0:
                return None
            else:
                return msgs

        except:
            logging.critical(_("MSG check error"))

        return None

    def msg_send(self, attr, body):
        try:
            m = RawMessage()
            m.message_attributes= attr
            m.set_body(body)

            self.q.set_message_class(RawMessage)
            self.q.write(m)
        except:
            logging.critical(_("Message creation failure: msg_send()"))

    def process_my_msg(self, func, msgs):
        try:
            if msgs is not None:
                length=len(msgs)

                for i in range(0, length):
                    msg = msgs[i]
                    if msg.message_attributes["to"]["string_value"] == "*" or msg.message_attributes["to"]["string_value"] == format(socket.gethostname()):
                        if self.msg_dict.get(msg.id, None) is None:
                            self.msg_dict[msg.id] = msg.attributes['ApproximateFirstReceiveTimestamp']
                            func(msg)
                        else:
                            logging.debug("Duplicate msg ...{0}".format(msg.id))

        except BaseException as e:
            logging.critical(_("MSG process error: process_my_msg() {0}").format(e))


    #Server
    def server_run(self):
        while True:
            try:
                msgs=self.msg_get_all()
                self.process_my_msg(lambda x: self.server_msg_process(x), msgs)
                time.sleep(int(self.key["AWS_POLL"]))

                for key, value in self.msg_dict.items():
                    days = (datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.fromtimestamp(int(value)/1000)).days
                    if days > 3:
                        del self.msg_dict[key]
                logging.debug("msg_dict->{0}".format(self.msg_dict))
            except:
                logging.critical("server_run->while")
                raise ()


    def server_msg_process(self, msg):
        try:
            if msg.message_attributes["cmd"]["string_value"] == "ping":
                logging.info("Processing ... {0}".format(msg.id))
                self.pong_send(msg.message_attributes["from"]["string_value"])
                if msg.message_attributes["to"]["string_value"] == format(socket.gethostname()):
                    self.q.delete_message(msg)

        except BaseException as e:
            logging.critical(_("MSG process error: server_cmd() {0}").format(e))

    #Client
    def client_print(self):
        try:
                msgs=self.msg_get_all()
                self.process_my_msg(lambda x: self.client_msg_process(x), msgs)
                time.sleep(5)
        except:
            raise ()


    def client_msg_process(self, msg):
        try:
            if msg.message_attributes["cmd"]["string_value"] == "pong":
                self.q.delete_message(msg)
                import datetime
                print("reply\t\t{0}\t\t{1}\t\t{2}".format(msg.message_attributes["from"]["string_value"],
                                                          msg.message_attributes["from-ip"]["string_value"],
                                                          self.get_time(int(msg.attributes['ApproximateFirstReceiveTimestamp']))
                                                          ))
                logging.debug("client_msg_process ApproximateFirstReceiveTimestamp {0}".format( msg.attributes['ApproximateFirstReceiveTimestamp']))

                #print(self.get_time(msg.attributes['ApproximateFirstReceiveTimestamp']))
                #print(datetime.datetime.fromtimestamp(time.time(int(msg.attributes["ApproximateFirstReceiveTimestamp"]))).strftime('%Y-%m-%d %H:%M:%S'))


        except BaseException as e:
            logging.critical(_("MSG process error: client_msg_process() {0}").format(e))


    #cmd
    def ping_send(self, count):
         try:

             import copy
             attr= copy.deepcopy(AWS._attr)
             attr["from"]["string_value"] = format(socket.gethostname())
             attr["from-ip"]["string_value"] = self.get_ip()
             attr["cmd"]["string_value"] = "ping"

             for i in range(0, count):
                 self.msg_send(attr, "ping")



         except:
             logging.critical(_("Message creation failure: ping_send()"))

    def pong_send(self, to):
         try:

             import copy
             attr= copy.deepcopy(AWS._attr)
             attr["from"]["string_value"] = format(socket.gethostname())
             attr["from-ip"]["string_value"] = self.get_ip()
             attr["to"]["string_value"] = to
             attr["cmd"]["string_value"] = "pong"

             self.msg_send(attr, "pong")

         except:
             logging.critical(_("Message creation failure"))


    #helper
    def get_ip(self):
        try:
            logging.debug("get_ip")
            import requests
            r= requests.get(r'http://jsonip.com')
            return format( r.json()['ip'])
        except:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("gmail.com",80))
                s.close()
                return format(s.getsockname()[0])
            except:
                return "0.0.0.0"

    def get_time(self, timestamp):
        try:
            return time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(timestamp/1000))
        except:
            return ""

    def ping(self, count, timeout):

        self.connect_sqs()
        print(_("Sending ping ..."))
        self.ping_send(count)
        print(_("Waiting for reply ..."))
        time.sleep(timeout)
        self.client_print()
        print(_("Timeout"))
