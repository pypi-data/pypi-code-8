# -*- coding: utf-8 -*-

import sys
import os
import json
from flask import Flask
from capybara import Capybara

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/info/<service>/", methods=['GET'])
def info(service):
    available = capy.isAvailable(service)
    if available:
        msg = ""
        msg += "Service %s is available!\n" % service
        msg += "Information:\n"
        msg += "\tconfig=%s, \n" % json.dumps(capy.wrappers[service].config)
        msg += "\ttokens=%s, \n" % len(capy.wrappers[service].tokens)
        msg += "\taccess_count=%s, \n" % capy.wrappers[service].access_count
        return msg
    else:
        return "Service %s is unavailable!" % service

@app.route("/get/<service>/<item>/", methods=['GET'])
def get(service, item):
    res = capy.get(service=service.strip(), item=item.strip())
    if res:
        return str(res)
    else:
        return "Unable to get item %s at %s. \nSee the log for detail." % (item, service)

# @app.route("/get/<service>/<item>/json", methods=['GET'])
# def get_json(service, item):
#     res = capy.get(service.strip(), item.strip())
#     if res:
#         return str(res)
#     else:
#         return "Unable to get item %s at %s. \nSee the log for detail." % (item, service)

@app.route("/get/<service>/<item>/<attr>/", methods=['GET'])
def get_title(service, item, attr):
    res = capy.get(service=service.strip(), item=item.strip())
    if res:
        return res[attr]
    else:
        return "Unable to get item %s at %s. \nSee the log for detail." % (item, service)

if __name__=="__main__":

    args = sys.argv
    argc = len(args)

    if argc == 1:
        config = os.path.join(os.getcwd(), "./config")
        tokens = os.path.join(os.getcwd(), "./tokens")
    elif argc == 3:
        config = os.path.join(os.getcwd(), args[1])
        tokens = os.path.join(os.getcwd(), args[2])
    else:
        print "Invalid number of arguments(%s)" % argc-1
        exit()

    capy = Capybara(config_dir=config, tokens_dir=tokens)

    app.run()
