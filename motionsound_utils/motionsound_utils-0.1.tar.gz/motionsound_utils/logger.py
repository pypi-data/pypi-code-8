__author__ = 'jiusi'

import parameters as param
# from mixpanel import Mixpanel
# mp = Mixpanel(param.MIX_PANEL_TOKEN)

from logentries import LogentriesHandler
import logging

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
# Note if you have set up the logentries handler in Django, the following line is not necessary
log.addHandler(LogentriesHandler('a6336037-db5d-4900-8cc6-707e7a3a6475'))

import utils
import json


def logMotionPrediction(apiName, rawData, result):
    logProperties = {}
    logProperties['apiName'] = apiName
    logProperties['rawData'] = rawData
    logProperties['result'] = result

    log.info(json.dumps(logProperties))


def logContextPrediction(apiName, soundSavePath, ctxPred, evnPreds):
    logProperties = {}
    logProperties['apiName'] = apiName
    logProperties['soundSavePath'] = soundSavePath
    logProperties['ctxPred'] = ctxPred
    logProperties['evnPreds'] = evnPreds

    log.info(json.dumps(logProperties))


def logTrainResult(trainStartTime, clfName, paramName, cScore, remapSavePath):
    logProperties = {}

    logProperties['trainStartTime'] = trainStartTime
    logProperties['clfName'] = clfName
    logProperties['paramName'] = paramName
    logProperties['cScore'] = cScore
    logProperties['remapSavePath'] = remapSavePath

    log.info(json.dumps(logProperties))
