__author__ = 'Alex Gomes'

from azure.storage import QueueService, TableService, Entity

import os, sys, logging, time, socket, pprint, time, datetime, json, base64
import alxlib.key
from gettext import gettext as _
from alxlib.node.info import Info
import alxlib.time_help as time_hep


logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("azure").setLevel(logging.CRITICAL)


class Azure():
    def __init__(self):
        self.tbl_name = 'alxserver'
        self.tbl_net = "net"
        self.tbl_info = "info"
        self.tbl_node = "node"

        self.q_name = 'alxserver'
        self.msg_delete_ids = {self.q_name: {},
                               }
        self.msg_no_process = {self.q_name: {},
                               }

        self.msg_template = {"from": "",
                             "from-ip": "",
                             "to": "",
                             "cmd": "",
                             }

        self.msg_key_na = _('Key not available')

        self.msg_ttl = 60 * 60

        self.msg_delete_ids_ttl = 60 * 60 * 3

        try:

            key = alxlib.key.Key()
            if os.path.isfile(key.get_path()):
                sys.path.insert(0, key.get_dir())

                import alxkey

                self.key = alxkey.alxkey_azure
                self.tbl = TableService(account_name=self.key['AZURE_STORAGE_ACCOUNT_NAME'],
                                        account_key=self.key['AZURE_ACCESS_KEY'])

            else:
                raise (self.msg_key_na)
        except:
            raise (self.msg_key_na)


    # Connection
    def connect_sqs(self):
        try:
            self.q = QueueService(account_name=self.key['AZURE_STORAGE_ACCOUNT_NAME'],
                                  account_key=self.key['AZURE_ACCESS_KEY'])

            self.q.create_queue(self.q_name)
            return self.q
        except:
            logging.critical(_("Connection Failure: possibly bad key"))
            return None

    # msg
    def msg_get_all(self):
        try:

            self.connect_sqs()
            msgs = self.q.peek_messages(self.q_name, numofmessages=16)

            queue_metadata = self.q.get_queue_metadata(self.q_name)
            count = queue_metadata['x-ms-approximate-messages-count']

            logging.info("Checking queue {0}, {1} message".format(self.q_name, count))

            if count == 0:
                return None
            else:
                return msgs

        except Exception as e:
            logging.critical(_("MSG check error"))

        return None

    def msg_send(self, dict):
        try:
            self.connect_sqs()
            body = self.msg_encode(dict)
            self.q.put_message(self.q_name, body, messagettl=self.msg_ttl)
            #print(encode.decode())

        except Exception as e:
            logging.critical(_("Message creation failure: msg_send()"))

    def msg_encode(self, dict):
        try:
            j = json.dumps(dict, ensure_ascii=False)
            body = base64.b64encode(j.encode()).decode()
            return body
        except Exception as e:
            logging.critical(_("Message creation failure: msg_encode()"))

    def msg_decode(self, body):
        try:
            dict = eval(base64.b64decode(body.encode()).decode())
            return dict
        except:
            logging.critical(_("Message decode failure: msg_decode()"))
            return None

    def msg_delete(self):
        try:
            if len(self.msg_delete_ids[self.q_name]) > 0:
                self.connect_sqs()
                msgs = self.q.get_messages(self.q_name, numofmessages=16)
                for msg in msgs:
                    if self.msg_delete_ids[self.q_name].get(msg.message_id, None) is not None:
                        self.q.delete_message(self.q_name, msg.message_id, msg.pop_receipt)
                        del self.msg_delete_ids[self.q_name][msg.message_id]
                        logging.info("Deleting msg {0}".format(msg.message_id))

                for key, value in self.msg_delete_ids[self.q_name].items():
                    seconds = (
                        datetime.datetime.fromtimestamp(self.get_timestamp_now()) - datetime.datetime.fromtimestamp(
                            float(value))).seconds
                    if seconds > self.msg_delete_ids_ttl:
                        del self.msg_delete_ids[self.q_name][key]

        except:
            logging.critical(_("Message delete failure: msg_delete()"))


    def process_my_msg(self, func, msgs):
        try:
            if msgs is not None:
                for msg in msgs:
                    body = msg.message_text
                    if body is not None:
                        dict = self.msg_decode(body)
                        if dict["to"] == "*" or dict["to"] == format(socket.gethostname()):
                            if self.msg_no_process[self.q_name].get(msg.message_id, None) is None:
                                self.msg_no_process[self.q_name][msg.message_id] = dict['creation-time']
                                func(msg, dict)
                            else:
                                logging.debug("Ignore msg ...{0}".format(msg.message_id))
        except BaseException as e:
            logging.critical(_("MSG process error: process_my_msg() {0}").format(e))


    #Server
    def server_run(self):
        while True:
            try:

                self.update_net()

                """

                msgs = self.msg_get_all()
                self.process_my_msg(lambda x, y: self.server_msg_process(x, y), msgs)
                time.sleep(int(self.key["AZURE_POLL"]))

                self.msg_delete()

                for key, value in self.msg_no_process[self.q_name].items():
                    seconds = (
                    datetime.datetime.fromtimestamp(self.get_timestamp_now()) - datetime.datetime.fromtimestamp(
                        float(value))).seconds
                    if seconds > self.msg_delete_ids_ttl:
                        del self.msg_no_process[self.q_name][key]
                logging.debug("msg_no_process->{0}".format(self.msg_no_process))"""


            except Exception as e:
                logging.critical("server_run->while {0}".format(e))
                #print(e)
                raise ()

    def server_msg_process(self, msg, dict):
        try:
            if dict["cmd"] == "ping":
                logging.info("Processing ... {0}".format(msg.message_id))
                self.pong_send(dict["from"], msg.message_id)
                if dict["to"] == format(socket.gethostname()):
                    #self.q.delete_message(self.q_name, msg.message_id, msg.pop_receipt)
                    self.msg_delete_ids[self.q_name][msg.message_id] = dict['creation-time']


        except BaseException as e:
            logging.critical(_("MSG process error: server_cmd() {0}").format(e))

    #Client
    def client_print(self):
        try:
            msgs = self.msg_get_all()
            self.process_my_msg(lambda x, y: self.client_msg_process(x, y), msgs)
            self.msg_delete()
            #time.sleep(5)
        except:
            raise ()

    def client_msg_process(self, msg, dict):
        try:
            if dict["cmd"] == "pong":
                self.msg_delete_ids[self.q_name][msg.message_id] = dict['creation-time']
                #self.q.delete_message(self.q_name, msg.message_id, msg.pop_receipt)
                import datetime

                print("reply\t\t{0}\t\t{1}\t\t{2}".format(dict["from"],
                                                          dict["from-ip"],
                                                          self.get_time(float(dict['creation-time']))
                                                          ))
                logging.debug("client_msg_process creation-time {0}".format(dict['creation-time']))

                #print(self.get_time(msg.attributes['ApproximateFirstReceiveTimestamp']))
                #print(datetime.datetime.fromtimestamp(time.time(int(msg.attributes["ApproximateFirstReceiveTimestamp"]))).strftime('%Y-%m-%d %H:%M:%S'))


        except BaseException as e:
            logging.critical(_("MSG process error: client_msg_process() {0}").format(e))


    #cmd
    def ping(self, count, timeout):

        self.connect_sqs()
        print(_("Sending ping ..."))
        self.ping_send(count)
        print(_("Waiting for reply ..."))
        time.sleep(timeout)
        self.client_print()
        print(_("Timeout"))

    def ping_send(self, count):
        try:

            import copy, alxlib.node.info

            dict = copy.deepcopy(self.msg_template)
            dict["from"] = format(socket.gethostname())
            dict["from-ip"] = alxlib.node.info.Info().get_ip()
            dict["to"] = "*"
            dict["cmd"] = "ping"
            dict["creation-time"] = str(self.get_timestamp_now())

            for i in range(0, count):
                self.msg_send(dict)

        except Exception as e:
            logging.critical(_("Message creation failure: ping_send()"))

    def pong_send(self, to, replyToId):
        try:

            import copy, alxlib.node.info

            dict = copy.deepcopy(self.msg_template)
            dict["from"] = format(socket.gethostname())
            dict["from-ip"] = alxlib.node.info.Info().get_ip()
            dict["to"] = to
            dict["reply-to-id"] = replyToId
            dict["cmd"] = "pong"
            dict['creation-time'] = str(self.get_timestamp_now())

            self.msg_send(dict)

        except:
            logging.critical(_("Message creation failure"))


    #helper

    def get_time(self, timestamp):
        try:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        except:
            return ""

    def get_timestamp_now(self):
        return time.time()

    #table

    def tbl_update(self, name, p, r, d):
        try:
            d["updatetime"] = str(self.get_timestamp_now())
            self.tbl.create_table(name)
            self.tbl.insert_or_merge_entity(name, p, r, d)
        except Exception as e:
            logging.critical("Error update_tbl {0}".format(e))


    def tbl_row_query(self, name, q, n=1000, next_partition_key_=None, next_row_key_=None):
        try:
            self.tbl.create_table(name)

            rows = self.tbl.query_entities(name, filter=q, top=n,
                                           next_partition_key=next_partition_key_,
                                           next_row_key=next_row_key_)
            return rows
        except Exception as e:
            return None

    def entity2dict(self, e):
        try:
            keys = dir(e)
            d = {}
            for key in keys:
                d[key] = getattr(e, key, "")
            return d
        except:
            return None

    def update_net(self):
        try:
            info = Info().get_all()
            self.tbl_update(self.tbl_name, self.tbl_net, info["hostname"], info)
        except:
            logging.warning("Error update_net")

    def wrap_text(self, text, max_width):
        if text is not None:
            from textwrap import wrap

            return '\n'.join(wrap(text, max_width))
        else:
            return ""


    def print_list(self):
        try:
            rows = self.tbl_row_query(self.tbl_name, "PartitionKey eq 'net'")
            #print(dir(row))

            from colorclass import Color, Windows

            from terminaltables import AsciiTable

            Windows.enable(auto_colors=True, reset_atexit=True)

            table_data = [[Color('{autocyan}Hostname'),
                           Color('{autocyan}Last Reply'),
                           Color('{autocyan}IP'),
                           Color('{autocyan}OS'),
                           Color('{autocyan}OS Release'),
                           Color('{autocyan}OS Version'),
                           Color('{autocyan}System'),
                           Color('{autocyan}Processor'),
                           ]
                          ]

            for row in rows:
                #d = self.entity2dict(row)
                d = row.__dict__
                time = alxlib.time_help.format_from_timestamp(d['Timestamp'])
                li = [d['hostname'], time, d['ip'], d['os'], d['osrelease'], d['osversion'], d["system"],
                      self.wrap_text(d["processor"], 10), ]
                table_data.append(li)

            table = AsciiTable(table_data)

            table.table_data = table_data

            print(table.table)
        except Exception as e:
            logging.warning("Error print_list")
            print(e)






