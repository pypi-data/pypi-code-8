__author__ = 'jiusi'

import time
import os

from utils import zipDir, unzipDir, emptyDir, isEmpty, getClfUploadPath
import parameters as param

import urllib2

def achieveProdClf(prodClfPath, achieveName):
    achievePath = param.clf_ACHI + achieveName
    zipDir(achievePath, prodClfPath)
    emptyDir(prodClfPath)
    if not isEmpty(prodClfPath):
        print 'remove error'
        raise Exception('remove production clf failed, deploy abort')


def achieveCtxClf():
    achieveName = str(int(time.time() * 1000)) + '.ach'
    prodClfPath = param.ctxClf_PROD_ROOT
    achieveProdClf(prodClfPath, achieveName)


def achieveEvnClf():
    achieveName = str(int(time.time() * 1000)) + '.ach'
    prodClfPath = param.evnClf_PROD_ROOT
    achieveProdClf(prodClfPath, achieveName)

def setupClfUpload(clfPath, clfUUID):
    uploadPath = getClfUploadPath(clfUUID)

    if os.path.exists(uploadPath):
        os.remove(uploadPath)

    zipDir(zipname=uploadPath, dir_to_zip=clfPath)

    return uploadPath

# predictor will download clf from trainer
def downloadClf(clfUUID):
    downloadUrl = "http://" + param.trainerIP + ':' + param.trainerPort + param.clfDownloadApi + clfUUID

    file_name = downloadUrl.split('/')[-1]
    u = urllib2.urlopen(downloadUrl)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

    return os.path.abspath(file_name)


def installClf(clfType, clfZipPath):

    if clfType == 'evn':
        achieveEvnClf()
        prodPath = param.evnClf_PROD_ROOT
    elif clfType == 'ctx':
        achieveCtxClf()
        prodPath = param.ctxClf_PROD_ROOT
    else:
        raise Exception('clf type error:' + clfType)

    unzipDir(clfZipPath, prodPath)
