__author__ = 'jiusi'
from sklearn.externals import joblib
import ntpath
import os
from os import path
import parameters as param
import uuid
import yaml
import shutil
import time
import errno
import numpy as np
import zipfile
import scipy.io.wavfile as wavfile
import json
from werkzeug.datastructures import FileStorage


def loadClassifier(clfPath):
    clf = joblib.load(clfPath)
    print 'classifier recovered from:', clfPath
    return clf


def saveClassifier(clf, savePath):
    dirName = os.path.dirname(savePath)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print 'savePath:', savePath, 'don not exist, os make dir called'

    s = joblib.dump(clf, savePath)
    print 'classifier saved at:', s


def saveJson(jsonData, savePath):
    dirName = os.path.dirname(savePath)

    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print 'savePath:', savePath, 'don not exist, os make dir called'

    with open(savePath, 'w') as outfile:
        json.dump(jsonData, outfile)
        print 'remap json saved at:', savePath


def loadJson(loadPath):
    with open(loadPath) as data_file:
        data = json.load(data_file)
        print 'json recovered from:', loadPath
        return data


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def saveUploadedFile(f, savePath):
    dirName = os.path.dirname(savePath)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print 'savePath:', savePath, 'don not exist, os make dir called'

    if isinstance(f, file):
        dest = open(savePath, 'wb+')
        for chunk in f.chunks():
            dest.write(chunk)
        dest.close()
    elif isinstance(f, FileStorage):
        f.save(savePath)
    print 'uploaded file save to:', savePath


def loadMotionClfs():
    moClfVH = loadClassifier(param.moClf_VH)
    moClfSS_L1 = loadClassifier(param.moClf_SS_L1)
    moClfSS_L2A = loadClassifier(param.moClf_SS_L2A)
    moClfSS_L2I = loadClassifier(param.moClf_SS_L2I)

    return moClfVH, moClfSS_L1, moClfSS_L2A, moClfSS_L2I


def loadByUUIDDict(uuidDict):
    clfDict = {}
    for key in uuidDict.keys():
        uuid = uuidDict[key]
        if key == 'clf':
            clfPath = getClfPathByUUID(uuid)
            clfDict[key] = loadClassifier(clfPath)
        elif key == 'remap':
            remapPath = getRemapPathByUUID(uuid)
            clfDict[key] = loadJson(remapPath)
        else:
            raise TypeError('load failed, key in uuid dict is not recognized:' + key)
    return clfDict


def loadMotionGMM():
    mo_ss_gmm = loadClassifier(param)


def loadContextClfs():
    ctxClfProd = loadClassifier(param.ctxClf_PROD)
    return ctxClfProd


def loadEventClfs():
    evnClfProd = loadClassifier(param.evnClf_PROD)
    return evnClfProd


def getCorrectRate(trueTags, pred):
    count = 0
    for trueTag, p in zip(trueTags, pred):
        if trueTag == p:
            count += 1
    return count / len(trueTags)


def genContextClfDir(clfType):
    return param.contextClfPrefix + '_' + clfType + '_' + str(uuid.uuid4()) + '/'


def genEventClfDir(clfType):
    return param.eventClfPrefix + '_' + clfType + '_' + str(uuid.uuid4()) + '/'


def genMitL1ClfDir(clfType):
    return param.mitL1ClfPrefix + '_' + clfType + '_' + str(uuid.uuid4()) + '/'


def genMotionClfDir():
    return str(uuid.uuid4()) + '/'

def genSoundClfDir():
    return str(uuid.uuid4()) + '/'


def genRemapJsonName():
    return str(uuid.uuid4()) + '.json'


def genContextParamFileName():
    return param.contextParamPrefix + '_' + str(uuid.uuid4()) + '.json'


def genMotionParamFileName():
    return param.motionParamPrefix + '_' + str(uuid.uuid4()) + '.json'


def genSoundFileName():
    return param.soundClipPrefix + '_' + str(uuid.uuid4()) + '.mp3'


def getFeatureParam4Ctx():
    fp = {}
    fp['N_MFCC'] = param.N_MFCC
    fp['FREQ_MAX'] = param.FREQ_MAX
    fp['CTX_FRAME_IN_SEC'] = param.CTX_FRAME_IN_SEC
    fp['EVN_FRAME_IN_SEC'] = param.EVN_FRAME_IN_SEC
    fp['FEATURES'] = param.FEATURES

    return fp


def getFeatureParam4Evt():
    fp = {}
    fp['N_MFCC'] = param.N_MFCC
    fp['FREQ_MAX'] = param.FREQ_MAX
    fp['FRAME_IN_SEC'] = param.EVN_FRAME_IN_SEC
    fp['FEATURES'] = param.FEATURES

    return fp


def getTrainParam4Ctx(paramSavePath):
    jsonData = open(paramSavePath)
    trainParam = yaml.load(jsonData)
    trainParam['FRAME_IN_SEC'] = trainParam['CTX_FRAME_IN_SEC']
    return trainParam


def getTrainParam4Evn(paramSavePath):
    jsonData = open(paramSavePath)
    trainParam = yaml.load(jsonData)
    trainParam['FRAME_IN_SEC'] = trainParam['EVN_FRAME_IN_SEC']
    return trainParam


def getTrainParam4MITL1(paramSavePath):
    jsonData = open(paramSavePath)
    trainParam = yaml.load(jsonData)
    trainParam['FRAME_IN_SEC'] = trainParam['MIT_FRAME_IN_SEC']
    return trainParam


def getTrainParam4Motion(paramSavePath):
    jsonData = open(paramSavePath)
    trainParam = yaml.load(jsonData)
    return trainParam


def writeWavfile(rate, data, savePath):
    data = np.asarray(data, dtype=np.int16)
    wavfile.write(savePath, rate, data)


def isMp3(fileName):
    if '.' in fileName:
        ext = fileName.rsplit('.', 1)[1]
        if ext.lower() == 'mp3':
            return True
    return False


def isJsonFile(fileName):
    if '.' in fileName:
        ext = fileName.rsplit('.', 1)[1]
        if ext.lower() == 'json':
            return True
    return False


def zipDir(zipname, dir_to_zip):
    dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
    with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for dirname, subdirs, files in os.walk(dir_to_zip):
            for filename in files:
                path = os.path.join(dirname, filename)
                entry = path[dir_to_zip_len:]
                zf.write(path, entry)


def unzipDir(zipname, dir_to_unzip):
    with zipfile.ZipFile(zipname) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target = file(os.path.join(dir_to_unzip, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)


def emptyDir(dir):
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


def isEmpty(dir):
    files = os.listdir(dir)
    for fileName in files:
        name, ext = os.path.splitext(fileName)
        if ext == '.clf':
            return False
    return True


def getDeployAPI(ip, port):
    return ip + ":" + port + param.deployUrl


def getClfPathByType(type, clfUUID):
    if type == 'evn':
        clfRoot = param.eventClfRoot
    elif type == 'ctx':
        clfRoot = param.contextClfRoot
    else:
        raise Exception('clf type incorrect')

    clfs = get_immediate_subdirectories(clfRoot)

    clfToFind = None
    for clf in clfs:
        thisUUID = clf.split('_')[-1]
        if thisUUID == clfUUID:
            clfToFind = clf
            break

    if not clfToFind:
        raise Exception('did not find clf uuid:' + clfUUID)

    clfAbsPath = clfRoot + clfToFind + 'clf.pkl'

    return clfAbsPath


def getClfPathByUUID(clfUUID):
    clfRoot = param.clfRoot
    clfDirPath = getDirByUUID(clfUUID, clfRoot) + 'clf.pkl'
    return clfDirPath


def getRemapPathByUUID(remapUUID):
    remapRoot = param.clfRoot
    remapFilePath = getFileByUUID(remapUUID, remapRoot)
    return remapFilePath


def getDirByUUID(uuid, rootDir):
    dirs = get_immediate_subdirectories(rootDir)

    dirToFind = None
    for dir in dirs:
        thisUUID = dir
        if thisUUID == uuid:
            dirToFind = uuid
            break

    if not dirToFind:
        raise Exception('did not find dir by uuid:' + uuid)

    dirAbsPath = rootDir + dirToFind + '/'
    return dirAbsPath


def getFileByUUID(uuid, rootDir):
    filenames = get_immediate_subfiles(rootDir)

    fileToFind = None
    for filename in filenames:
        thisUUID = filename.split('.')[0]
        if thisUUID == uuid:
            fileToFind = filename
            break

    if not fileToFind:
        raise Exception('did not find file by uuid:' + uuid)

    fileAbsPath = rootDir + fileToFind
    return fileAbsPath


def getClfUploadPath(clfUUID):
    uploadPath = param.clf_UP + clfUUID + '.zip'
    return uploadPath


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_immediate_subfiles(a_dir):
    return next(os.walk(a_dir))[2]


def clfIsUnsupervised(clfType):
    if 'gmm' in clfType.lower():
        return True

    return False