#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flask based API.
    Requires ircsend to work.
    Probably won't work on systems that has not the base config added.
"""

from flask import Flask, render_template
from scipy.spatial import distance

import subprocess
import json
import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_FILE = os.path.join(BASE_DIR, "magic_lightning.conf")
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
COLORS_FILE = os.path.join(BASE_DIR, 'base_colors.json')


def get_base_colors():
    """
        Extracts base config from a json.
        Color format is [rrr,ggg,bbb] (0..255)
        The buttons configured in CONF_FILE with irrecord must be named
        rrr_ggg_bbb as in the json file
    """
    return [tuple(color) for color in json.load(open(COLORS_FILE))]


BASE_COLORS = get_base_colors()
APP = Flask(__name__, template_folder=TEMPLATES_DIR)


@APP.route("/")
def index():
    """
        Main template
    """
    return render_template('main.html')


@APP.route('/change_color/<color>')
def change_light(color):
    """
        Change light color.

        It takes a comma-separated RGB vector [RRR, GGG, BBB] (0..255)
        and returns the closest value from the json's color vectors calculating
        its euclidean distance.

        This way we can use a generic colorpicker and return the color
        that the lamp supports
    """
    distances = []
    curr_color = tuple(map(int, color.split(',')))

    for color in BASE_COLORS:
        distances.append([color, distance.euclidean(color, curr_color)])

    distances_sorted = list(sorted(distances, key=lambda x: x[1])[0][0])
    closest = '_'.join(map(str, distances_sorted))
    res = subprocess.check_call(['irsend', 'SEND_ONCE', CONF_FILE, closest])

    return json.dumps({"key": closest, 'result': res})


@APP.route('/action/<action>')
def action(action_):
    """
        Executes a custom action.
    """
    result = subprocess.check_call(['irsend', 'SEND_ONCE', CONF_FILE, action_])
    return json.dumps({"key": action_, 'result': result})


def main():
    """
        Run app
    """
    APP.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    main()
