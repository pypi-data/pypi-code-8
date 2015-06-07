# -*- coding: utf-8 -*-

from daemon import Daemon
from time import sleep
from .config import Config
from .task import Task

import subprocess
import requests
import urllib2
import json
import os

def launch():
    global config
    interval = config.interval
    tasks = Task(config)

    while True:
        # update from server
        tasks.get_updates() # check whether have new updates

        # run tasks
        # run all task (including old tasks) & save result
        tasks.run_and_save_result()

        # send result to center
        if tasks.send_back_result() is False:
            times = 1;
            while (times < 10):
                sleep(10 + 2 * 10)
                if tasks.send_again():
                    break

        # set interval for next run
        interval = tasks.get_interval()
        config.set_interval(interval)
        tasks.sleep()

def EmpireAgent(Daemon):
    def run(self):
        launch()
