#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright 2013 Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from .filesystem_assetstore_adapter import FilesystemAssetstoreAdapter
from .gridfs_assetstore_adapter import GridFsAssetstoreAdapter
from .s3_assetstore_adapter import S3AssetstoreAdapter
from girder.constants import AssetstoreType
from girder import events


def getAssetstoreAdapter(assetstore, instance=True):
    """
    This is a factory method that will return the appropriate assetstore adapter
    for the specified assetstore. The returned object will conform to
    the interface of the AbstractAssetstoreAdapter.

    :param assetstore: The assetstore document used to instantiate the adapter.
    :type assetstore: dict
    :param instance: Whether to return an instance of the adapter or the class.
        If you are performing validation, set this to False to avoid throwing
        unwanted exceptions during instantiation.
    :type instance: bool
    :returns: An adapter descending from AbstractAssetstoreAdapter
    """
    cls = None
    storeType = assetstore['type']

    if storeType == AssetstoreType.FILESYSTEM:
        cls = FilesystemAssetstoreAdapter
    elif storeType == AssetstoreType.GRIDFS:
        cls = GridFsAssetstoreAdapter
    elif storeType == AssetstoreType.S3:
        cls = S3AssetstoreAdapter
    else:
        e = events.trigger('assetstore.adapter.get', assetstore)
        if len(e.responses) > 0:
            cls = e.responses[-1]
        else:
            raise Exception('No AssetstoreAdapter for type: %s.' % storeType)

    if instance:
        return cls(assetstore)
    else:
        return cls


def fileIndexFields():
    """
    This will return a set of all required index fields from all of the
    different assetstore types.
    """
    return list(set(
        FilesystemAssetstoreAdapter.fileIndexFields() +
        GridFsAssetstoreAdapter.fileIndexFields() +
        S3AssetstoreAdapter.fileIndexFields()
    ))
