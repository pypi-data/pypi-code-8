import os
import IPython
import sys
import random

PASS_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "pass"
FAIL_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "fail"
START_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "start"

def run():
    wins = os.listdir(PASS_DIR)
    fails = os.listdir(FAIL_DIR)
    starts = os.listdir(START_DIR)

    if sys.argv[1] == "pass":
        sound = PASS_DIR + os.sep + wins[random.randint(0, len(wins) - 1)]
        os.system("mplayer -msglevel all=-1 {} > /dev/null 2>&1 &".format(sound))
    elif sys.argv[1] == "fail":
        sound = FAIL_DIR + os.sep + fails[random.randint(0, len(fails) - 1)]
        os.system("mplayer -msglevel all=-1 {} > /dev/null 2>&1 &".format(sound))
    elif sys.argv[1] == "start":
        sound = START_DIR + os.sep + starts[random.randint(0, len(starts) - 1)]
        os.system("mplayer -msglevel all=-1 {} > /dev/null 2>&1 &".format(sound))
    else:
        print "Usage: kaching [pass | fail | start]"

