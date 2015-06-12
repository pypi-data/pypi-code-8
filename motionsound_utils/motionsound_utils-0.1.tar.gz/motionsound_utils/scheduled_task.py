__author__ = 'jiusi'

import config
import parameters as param
import glob

import time
import os.path
import datetime

import sched

def removeExpFiles():
    audioDir = param.requestSoundClipsRoot
    mp3List = glob.glob(audioDir + '*.mp3')
    m4aList = glob.glob(audioDir + '*.m4a')
    wavList = glob.glob(audioDir + '*.wav')

    fileList = mp3List.extend(m4aList)
    fileList = fileList.extend(wavList)
    counter = 0

    for filePath in fileList:
        if expired(filePath, config.audioExpTimeInHrs * 3600):
            os.remove(filePath)
            counter += 1

    return counter


def expired(filePath, expTime):
    createdAt = os.path.getmtime(filePath)
    expPoint = createdAt - expTime

    if time.time() < expPoint:
        return True
    else:
        return False


def startFileClean():
    while True:
        print 'start clean files, time:', datetime.datetime(datetime.datetime.now())
        removeExpFiles()
        time.sleep(config.audioFileExpCheckDurationInHrs * 3600)
