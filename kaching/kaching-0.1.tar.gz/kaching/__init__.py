import os
import IPython
import sys
import random

__version__ = "0.1"

PASS_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "pass"
FAIL_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "fail"

def run():
    wins = os.listdir(PASS_DIR)
    fails = os.listdir(FAIL_DIR)

    if sys.argv[1] == "pass":
        sound = PASS_DIR + os.sep + wins[random.randint(0, len(wins) - 1)]
        os.system("mplayer {}".format(sound))
    elif sys.argv[1] == "fail":
        sound = FAIL_DIR + os.sep + fails[random.randint(0, len(fails) - 1)]
        os.system("mplayer {}".format(sound))
    else:
        print "Usage: kaching [pass | fail]"

