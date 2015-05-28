# Copyright 2014 Algolia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Receives documents from the oplog worker threads and indexes them
    into the backend.

    This file is a document manager for the Algolia search engine.
    """

import logging
import re
import json
from datetime import datetime
import bson.json_util as bsjson
import bson
import copy
import urllib3

from algoliasearch import algoliasearch
from mongo_connector import errors
from mongo_connector.util import exception_wrapper, retry_until_ok
from mongo_connector.doc_managers.doc_manager_base import DocManagerBase
from mongo_connector.doc_managers.formatters import DefaultDocumentFormatter

wrap_exceptions = exception_wrapper({
    algoliasearch.AlgoliaException: errors.ConnectionFailed,
    urllib3.exceptions.MaxRetryError: errors.OperationFailed
    })

from mongo_connector.constants import (DEFAULT_COMMIT_INTERVAL,
                                       DEFAULT_MAX_BULK)

from threading import Timer, RLock

LOG = logging.getLogger(__name__)

decoder = json.JSONDecoder()

class DocManager(DocManagerBase):
    """The DocManager class creates a connection to the Algolia engine and
        adds/removes documents, and in the case of rollback, searches for them.
        Algolia's native 'objectID' field is used to store the unique_key.
        """

    def __init__(self, url, auto_commit_interval=DEFAULT_COMMIT_INTERVAL,
                 unique_key='_id', chunk_size=DEFAULT_MAX_BULK,
                 meta_index_name="mongodb_meta", meta_type="mongodb_meta",
                 attachment_field="content", **kwargs):
        """The DocManager class creates a connection to the Algolia engine and
            adds/removes documents, and in the case of rollback, searches for them.

            Algolia's native 'objectID' field is used to store the unique_key.
            """
        application_id, api_key, index = url.split(':')
        self.algolia = algoliasearch.Client(application_id, api_key)
        self.index = self.algolia.initIndex(index)
        self.unique_key = unique_key
        self.chunk_size = chunk_size
        self.auto_commit = kwargs.pop('auto_commit', True)
        self.auto_commit_interval = auto_commit_interval
        if self.auto_commit_interval not in [None, 0]:
            self.run_auto_commit()
        self.last_object_id = None
        self.batch = []
        self.mutex = RLock()
        try:
            json = open("algolia_fields_" + index + ".json", 'r')
            self.attributes_filter = decoder.decode(json.read())
            LOG.info("Algolia Connector: Start with filter.")
        except IOError:  # No "fields" filter file
            self.attributes_filter = None
            LOG.info("Algolia Connector: Start without filter.")
        try:
            json = open("algolia_remap_" + index + ".json", 'r')
            self.attributes_remap = decoder.decode(json.read())
            LOG.info("Algolia Connector: Start with remapper.")
        except IOError:  # No "remap" filter file
            self.attributes_remap = None
            LOG.info("Algolia Connector: Start without remapper.")
        try:
            f = open("algolia_postproc_" + index + ".py", 'r')
            self.postproc = f.read()
            LOG.info("Algolia Connector: Start with post processing.")
        except IOError:  # No "postproc" filter file
            self.postproc = None
            LOG.info("Algolia Connector: Start without post processing.")


    def stop(self):
        """ Stops the instance """
        self.auto_commit = False

    def apply_remap(self, doc):
        """Copy the values of user-defined fields from the source document to
            user-defined fields in a new target document, then return the
            targetdocument.
            """
        if not self.attributes_remap:
            return doc
        remapped_doc = {}
        for raw_source_key, raw_target_key in self.attributes_remap.items():
            # clean the keys, making a list from possible notations:
            source_key = clean_path(raw_source_key)
            target_key = clean_path(raw_target_key)

            # get the value from the source doc:
            value = get_at(doc, source_key)

            # special case for "_ts" field:
            if source_key == ['_ts'] and target_key == ["*ts*"]:
                value = value if value else str(unix_time_millis())

            set_at(remapped_doc, target_key, value)
        return remapped_doc

    def apply_filter(self, doc, filter):
        """Recursively copy the values of user-defined fields from the source
            document to a new target document by testing each value against a
            corresponding user-defined expression. If the expression returns
            true for a given value, copy that value to the corresponding field
            in the target document. If the special `*all*` filter is used for
            a given document and an adjacent field's expression returns false
            for a given value, remove the document containing that field from
            its p
            """
        if not filter:
            # alway return a new object:
            return (copy.deepcopy(doc), True)
        filtered_doc = {}
        all_or_nothing = '*all*' in filter
        try:
            items = filter.iteritems()
        except AttributeError:
            items = filter.items();
        for raw_key, expr in items:
            if raw_key == '*all*':
                continue
            key = clean_path(raw_key)
            values = get_at(doc, key)
            state = True
            if type(values) == list:
                append = True
                set_at(filtered_doc, key, [])
            else:
                append = False
                values = [values]
            for value in values:
                if isinstance(value, dict):
                    sub, sub_state = self.apply_filter(value, filter[raw_key])
                    if sub_state:
                        put_at(filtered_doc, key, self.serialize(sub), append)
                    elif all_or_nothing:
                        node = get_at(filtered_doc, key[:-1])
                        del node[key[-1]]
                        return filtered_doc, False
                elif filter_value(value, filter[raw_key]):
                    put_at(filtered_doc, key, self.serialize(value), append)
                elif all_or_nothing:
                    return filtered_doc, False
                else:
                    state = False
        return (filtered_doc, state)

    def apply_update(self, doc, update_spec):
        doc = super(DocManager, self).apply_update(doc, update_spec)
        if "$unset" in update_spec:
            for attr in update_spec["$unset"]:
                if update_spec["$unset"][attr]:
                    doc[attr] = None
        return doc

    def update(self, document_id, update_spec, namespace, timestamp):
        """ Update document"""
        doc = self.index.getObject(str(document_id))
        self.upsert(self.apply_update(doc, update_spec), namespace, timestamp, True )

    def upsert(self, doc, namespace, timestamp, update = False):
        """ Update or insert a document into Algolia
        """
        with self.mutex:
            self.last_object_id = self.serialize(doc[self.unique_key])
            filtered_doc, state = self.apply_filter(self.apply_remap(doc),
                                                    self.attributes_filter)
            filtered_doc['objectID'] = self.last_object_id

            #if not state:  # delete in case of update
            #    self.batch.append({'action': 'deleteObject',
            #                       'body': {'objectID': last_object_id}})
            #    return

            if self.postproc is not None:
                exec(re.sub(r"_\$", "filtered_doc", self.postproc))

            self.batch.append({'action': 'partialUpdateObject' if update else 'addObject', 'body': filtered_doc})
            if len(self.batch) >= self.chunk_size:
                self.commit()

    def remove(self, document_id, namespace, timestamp):
        """ Removes documents from Algolia
        """
        with self.mutex:
            self.batch.append(
                {'action': 'deleteObject',
                 'body': {'objectID': str(document_id)}})
            if len(self.batch) >= self.chunk_size:
                self.commit()


    def search(self, start_ts, end_ts):
        """ Called to query Algolia for documents in a time range.
        """
        try:
            params = {
                'numericFilters': '_ts>=%d,_ts<=%d' % (start_ts, end_ts),
                'exhaustive': True,
                'hitsPerPage': 100000000
            }
            return self.index.search('', params)['hits']
        except algoliasearch.AlgoliaException as e:
            raise errors.ConnectionFailed(
                "Could not connect to Algolia Search: %s" % e)

    def commit(self, synchronous=False):
        """ Send the current batch of updates
        """
        try:
            request = {}
            with self.mutex:
                if len(self.batch) == 0:
                    return
                self.index.batch({'requests': self.batch})
                res = self.index.setSettings({'userData': {'lastObjectID': self.last_object_id}})
                self.batch = []
                if synchronous:
                    self.index.waitTask(res['taskID'])
        except (algoliasearch.AlgoliaException, urllib3.exceptions.MaxRetryError) as e:
            raise errors.OperationFailed(
                "Could not connect to Algolia Search: %s" % e)

    @wrap_exceptions
    def handle_command(self, doc, namespace, timestamp):
        db = namespace.split('.', 1)[0]
        if doc.get('dropDatabase'):
            raise errors.OperationFailed(
                "algolia_doc_manager does not support renaming a dropDatabase.")
        if doc.get('renameCollection'):
            #TODO rename an index
            LOG.warning(doc)
        if doc.get('create'):
            db, coll = self.command_helper.map_collection(db, doc['create'])
            if db and coll:
                LOG.warning(doc)
                #TODO create an index
        if doc.get('drop'):
            db, coll = self.command_helper.map_collection(db, doc['drop'])
            if db and coll:
                LOG.warning(doc)
                # TODO drop an index

    def run_auto_commit(self):
        """ Periodically commits to Algolia.
        """
        try:
            self.commit(True)
        except Exception as e:
            LOG.warning(e)
        if self.auto_commit:
            Timer(self.auto_commit_interval, self.run_auto_commit).start()

    @wrap_exceptions
    def get_last_doc(self):
        """ Returns the last document stored in Algolia.
        """
        last_object_id = self.get_last_object_id()
        if last_object_id is None:
            return None
        try:
            return self.index.getObject(str(last_object_id))
        except algoliasearch.AlgoliaException as e:
            raise errors.ConnectionFailed(
                "Could not connect to Algolia Search: %s" % e)

    @wrap_exceptions
    def get_last_object_id(self):
        """ Returns the last document ID stored in Algolia.
        """
        try:
            return (self.index.getSettings().get('userData', {})).get('lastObjectID', None)
        except algoliasearch.AlgoliaException as e:
            raise errors.ConnectionFailed(
                "Could not connect to Algolia Search: %s" % e)

    def clean_path(dirty):
        """Convert a string of python subscript notation or mongo dot-notation to a
            list of strings.
            """
        # handle python dictionary subscription style, e.g. `"['key1']['key2']"`:
        if re.match(r'^\[', dirty):
            return re.split(r'\'\]\[\'', re.sub(r'^\[\'|\'\]$', '', dirty))
        # handle mongo op dot-notation style, e.g. `"key1.key2"`:
        return dirty.split('.')

    def get_at(doc, path, create_anyway=False):
        """Get the value, if any, of the document at the given path, optionally
            mutating the document to create nested dictionaries as necessary.
            """
        node = doc
        last = len(path) - 1
        if last == 0:
            return doc.get(path[0])
        for index, edge in enumerate(path):
            if edge in node:
                node = node[edge]
            elif index == last or not create_anyway:
                # the key doesn't exist, and this is the end of the path:
                return None
            else:
                # create anyway will create any missing nodes:
                node = node[edge] = {}
        return node

    def set_at(doc, path, value):
        """Set the value of the document at the given path."""
        node = get_at(doc, path[:-1], create_anyway=True)
        node[path[-1]] = value

    def put_at(doc, path, value, append=False):
        """Set or append the given value to the document at the given path"""
        if append:
            get_at(doc, path).append(value)
        else:
            set_at(doc, path, value)

    def unix_time(dt=datetime.now()):
        epoch = datetime.utcfromtimestamp(0)
        delta = dt - epoch
        return delta.total_seconds()

    def unix_time_millis(dt=datetime.now()):
        return int(round(unix_time(dt) * 1000.0))

    def serialize(self, value):
        """If the value is an BSON ObjectId, cast it to a string."""
        if isinstance(value, bson.objectid.ObjectId):
            return str(value)
        else:
            return value

    @wrap_exceptions
    def filter_value(self, value, expr):
        """Evaluate the given expression in the context of the given value."""
        if expr == "":
            return True
        try:
            return eval(re.sub(r'\$_', 'value', expr))
        except Exception as e:
            LOG.warn("""
                Error raised from expression: {filter} with value {value}
                """.format(**locals()))
            LOG.warn(e)
            # return false to prevent potentially sensitive data from being synced:
            return False
