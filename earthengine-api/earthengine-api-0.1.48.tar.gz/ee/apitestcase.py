"""A TestCase that initializes the library with standard API methods."""



import unittest

import ee


class ApiTestCase(unittest.TestCase):

  def setUp(self):
    self.InitializeApi()

  def InitializeApi(self):
    """Initializes the library with standard API methods.

    This is normally invoked during setUp(), but subclasses may invoke
    it manually instead if they prefer.
    """
    self.last_download_call = None
    self.last_thumb_call = None
    self.last_table_call = None

    def MockSend(path, params, unused_method=None, unused_raw=None):
      if path == '/algorithms':
        return BUILTIN_FUNCTIONS
      elif path == '/value':
        return {'value': 'fakeValue'}
      elif path == '/mapid':
        return {'mapid': 'fakeMapId'}
      elif path == '/download':
        # Hang on to the call arguments.
        self.last_download_call = {'url': path, 'data': params}
        return {'docid': '1', 'token': '2'}
      elif path == '/thumb':
        # Hang on to the call arguments.
        self.last_thumb_call = {'url': path, 'data': params}
        return {'thumbid': '3', 'token': '4'}
      elif path == '/table':
        # Hang on to the call arguments.
        self.last_table_call = {'url': path, 'data': params}
        return {'docid': '5', 'token': '6'}
      else:
        raise Exception('Unexpected API call to %s with %s' % (path, params))
    ee.data.send_ = MockSend

    ee.Reset()
    ee.Initialize(None, '')


BUILTIN_FUNCTIONS = {
    'Image.constant': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'value',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.load': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'id',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'version',
                'type': 'Long'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.addBands': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'dstImg',
                'type': 'Image'
            },
            {
                'description': '',
                'name': 'srcImg',
                'type': 'Image'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'names',
                'type': 'List<String>'
            },
            {
                'default': False,
                'description': '',
                'optional': True,
                'name': 'overwrite',
                'type': 'boolean'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.clip': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'input',
                'type': 'Image'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geometry',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.select': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'input',
                'type': 'Image'
            },
            {
                'description': '',
                'name': 'bandSelectors',
                'type': 'List<Object>'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'newNames',
                'type': 'List<String>'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.parseExpression': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'expression',
                'type': 'String'
            },
            {
                'default': 'image',
                'description': '',
                'optional': True,
                'name': 'argName',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'vars',
                'type': 'List<String>'
            }
        ],
        'description': '',
        'returns': 'Algorithm'
    },
    'Feature': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geometry',
                'type': 'Geometry'
            },
            {
                'default': {},
                'description': '',
                'optional': True,
                'name': 'metadata',
                'type': 'Dictionary<Object>'
            }
        ],
        'description': '',
        'returns': 'Feature'
    },
    'Feature.get': {
        'type': 'Algorithm',
        'returns': '<any>',
        'hidden': False,
        'args': [
            {
                'type': 'Element',
                'description': '',
                'name': 'object'
            },
            {
                'type': 'String',
                'description': '',
                'name': 'property'
            }
        ],
        'description': ''
    },
    'Collection': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'features',
                'type': 'List<Feature>'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.loadTable': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'tableId',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geometryColumn',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'version',
                'type': 'Long'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.filter': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'filter',
                'type': 'Filter'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.limit': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'default': -1,
                'description': '',
                'optional': True,
                'name': 'limit',
                'type': 'int'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'key',
                'type': 'String'
            },
            {
                'default': True,
                'description': '',
                'optional': True,
                'name': 'ascending',
                'type': 'boolean'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.map': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'baseAlgorithm',
                'type': 'Algorithm'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'dynamicArgs',
                'type': 'Dictionary<String>'
            },
            {
                'default': {},
                'description': '',
                'optional': True,
                'name': 'constantArgs',
                'type': 'Dictionary<Object>'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'destination',
                'type': 'String'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.iterate': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'function',
                'type': 'Algorithm'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'first',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Object',
    },
    'ImageCollection.load': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'id',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'version',
                'type': 'Long'
            }
        ],
        'description': '',
        'returns': 'ImageCollection'
    },
    'ImageCollection.fromImages': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'images',
                'type': 'List<Image>'
            }
        ],
        'description': '',
        'returns': 'ImageCollection'
    },
    'ImageCollection.mosaic': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'ImageCollection'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Collection.geometry': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'default': {
                    'type': 'ErrorMargin',
                    'unit': 'meters',
                    'value': 0
                },
                'description': '',
                'optional': True,
                'name': 'maxError',
                'type': 'ErrorMargin'
            }
        ],
        'description': '',
        'returns': 'Geometry'
    },
    'Collection.draw': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'color',
                'type': 'String'
            },
            {
                'default': 3,
                'description': '',
                'optional': True,
                'name': 'pointRadius',
                'type': 'int'
            },
            {
                'default': 2,
                'description': '',
                'optional': True,
                'name': 'strokeWidth',
                'type': 'int'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'DateRange': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'start',
                'type': 'Date'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'end',
                'type': 'Date'
            }
        ],
        'description': '',
        'returns': 'DateRange'
    },
    'Date': {
        'returns': 'Date',
        'hidden': False,
        'args': [
            {
                'type': 'Object',
                'description': '',
                'name': 'value'
            },
            {
                'type': 'String',
                'default': None,
                'description': '',
                'optional': True,
                'name': 'timeZone'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'ErrorMargin': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'value',
                'type': 'Double'
            },
            {
                'default': 'meters',
                'description': '',
                'optional': True,
                'name': 'unit',
                'type': 'String'
            }
        ],
        'description': '',
        'returns': 'ErrorMargin'
    },
    'Filter.intersects': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            },
            {
                'default': {
                    'type': 'ErrorMargin',
                    'unit': 'meters',
                    'value': 0.1
                },
                'description': '',
                'optional': True,
                'name': 'maxError',
                'type': 'ErrorMargin'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.dateRangeContains': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.or': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'filters',
                'type': 'List<Filter>'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.and': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'filters',
                'type': 'List<Filter>'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.not': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'filter',
                'type': 'Filter'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.equals': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.lessThan': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.greaterThan': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.stringContains': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.stringStartsWith': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.stringEndsWith': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.listContains': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Image.mask': {
        'type': 'Algorithm',
        'args': [
            {
                'name': 'image',
                'type': 'Image',
                'description': ''
            },
            {
                'name': 'mask',
                'type': 'Image',
                'description': '',
                'optional': True,
                'default': None
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    # These two functions (Dictionary.get and Image.reduceRegion) are here
    # to force the creation of the Dictionary class.
    'Dictionary.get': {
        'returns': 'Object',
        'args': [
            {
                'type': 'Dictionary<Object>',
                'description': '',
                'name': 'map'
                },
            {
                'type': 'String',
                'description': '',
                'name': 'property'
                }
            ],
        'type': 'Algorithm',
        'description': '',
    },
    'Image.reduceRegion': {
        'returns': 'Dictionary<Object>',
        'hidden': False,
        'args': [
            {
                'type': 'Image',
                'description': '',
                'name': 'image'
            },
            {
                'type': 'ReducerOld',
                'description': '',
                'name': 'reducer'
            },
            {
                'default': None,
                'type': 'Geometry',
                'optional': True,
                'description': '',
                'name': 'geometry'
            },
            {
                'default': None,
                'type': 'Double',
                'optional': True,
                'description': '',
                'name': 'scale'
            },
            {
                'default': 'EPSG:4326',
                'type': 'String',
                'optional': True,
                'description': '',
                'name': 'crs'
            },
            {
                'default': None,
                'type': 'double[]',
                'optional': True,
                'description': '',
                'name': 'crsTransform'
            },
            {
                'default': False,
                'type': 'boolean',
                'optional': True,
                'description': '',
                'name': 'bestEffort'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    # Algorithms for testing ee.String.
    'String': {
        'returns': 'String',
        'hidden': False,
        'args': [
            {
                'type': 'Object',
                'description': '',
                'name': 'input'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'String.cat': {
        'returns': 'String',
        'hidden': False,
        'args': [
            {
                'type': 'String',
                'description': '',
                'name': 'string1'
            },
            {
                'type': 'String',
                'description': '',
                'name': 'string2'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    # An algorithm for testing computed Geometries.
    'Geometry.bounds': {
        'returns': 'Geometry',
        'hidden': False,
        'args': [
            {
                'type': 'Geometry',
                'description': '',
                'name': 'geometry'
            },
            {
                'default': None,
                'type': 'ErrorMargin',
                'optional': True,
                'description': '',
                'name': 'maxError'
            },
            {
                'default': None,
                'type': 'Projection',
                'optional': True,
                'description': '',
                'name': 'proj'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'Geometry.centroid': {
        'returns': 'Geometry',
        'args': [
            {
                'description': '',
                'name': 'geometry',
                'type': 'Geometry'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'maxError',
                'type': 'ErrorMargin'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'proj',
                'type': 'Projection'
            }
        ],
        'description': '',
        'type': 'Algorithm',
    },
    # Element property setting, used by the client-side override.
    'Element.set': {
        'returns': 'Element',
        'hidden': False,
        'args': [
            {
                'type': 'Element',
                'description': '',
                'name': 'object'
            },
            {
                'type': 'String',
                'description': '',
                'name': 'key'
            },
            {
                'type': 'Object',
                'description': '',
                'name': 'value'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'Element.setMulti': {
        'returns': 'Element',
        'hidden': False,
        'args': [
            {
                'type': 'Element',
                'description': '',
                'name': 'object'
            },
            {
                'type': 'Dictionary<Object>',
                'description': '',
                'name': 'properties'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'Image.geometry': {
        'returns': 'Geometry',
        'args': [
            {
                'description': '',
                'name': 'feature',
                'type': 'Element'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'maxError',
                'type': 'ErrorMargin'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'proj',
                'type': 'Projection'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geodesics',
                'type': 'Boolean'
            }
        ],
        'type': 'Algorithm',
        'description': '',
    },
    'Number.add': {
        'returns': 'Number',
        'hidden': False,
        'args': [
            {
                'type': 'Number',
                'description': '',
                'name': 'left'
            },
            {
                'type': 'Number',
                'description': '',
                'name': 'right'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'Array': {
        'returns': 'Array',
        'hidden': False,
        'args': [
            {
                'name': 'values',
                'type': 'Object'
            },
            {
                'name': 'pixelType',
                'type': 'PixelType',
                'optional': True,
                'default': None
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
    'List.slice': {
        'returns': 'List<Object>',
        'args': [
            {
                'type': 'List<Object>',
                'name': 'list'
            },
            {
                'type': 'Integer',
                'name': 'start'
            },
            {
                'default': None,
                'type': 'Integer',
                'optional': True,
                'name': 'end'
            }
        ],
        'type': 'Algorithm',
        'description': '',
    },
    'List.map': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'list',
                'type': 'List'
            },
            {
                'description': '',
                'name': 'baseAlgorithm',
                'type': 'Algorithm'
            },
        ],
        'description': '',
        'returns': 'List'
    },
    'Projection': {
        'returns': 'Projection',
        'type': 'Algorithm',
        'description': '',
        'args': [
            {
                'name': 'crs',
                'type': 'Object',
                'description': ''
            },
            {
                'name': 'transform',
                'default': None,
                'type': 'List<Number>',
                'optional': True,
                'description': ''
            },
            {
                'name': 'transformWkt',
                'default': None,
                'type': 'String',
                'optional': True,
                'description': '',
            }
        ]
    },
    'Image.cast': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'image',
                'type': 'Image'
            },
            {
                'description': '',
                'name': 'bandTypes',
                'type': 'Dictionary'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'bandOrder',
                'type': 'List'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Describe': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'input',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Object',
    },
}

# A sample of encoded EE API JSON, used by SerializerTest and DeserializerTest.
ENCODED_JSON_SAMPLE = {
    'type': 'CompoundValue',
    'scope': [
        ['0', {
            'type': 'Invocation',
            'functionName': 'Date',
            'arguments': {
                'value': 1234567890000
            }
        }],
        ['1', {
            'type': 'LineString',
            'coordinates': [[1, 2], [3, 4]],
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'SR-ORG:6974'
                }
            }
        }],
        ['2', {
            'type': 'Polygon',
            'coordinates': [
                [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],
                [[5, 6], [7, 6], [7, 8], [5, 8]],
                [[1, 1], [2, 1], [2, 2], [1, 2]]
            ]
        }],
        ['3', {
            'type': 'Bytes',
            'value': 'aGVsbG8='
        }],
        ['4', {
            'type': 'Invocation',
            'functionName': 'String.cat',
            'arguments': {
                'string1': 'x',
                'string2': 'y'
            }
        }],
        ['5', {
            'type': 'Dictionary',
            'value': {
                'foo': 'bar',
                'baz': {'type': 'ValueRef', 'value': '4'}
            }
        }],
        ['6', {
            'type': 'Function',
            'argumentNames': ['x', 'y'],
            'body': {'type': 'ArgumentRef', 'value': 'y'}
        }],
        ['7', [
            None,
            True,
            5,
            7,
            3.4,
            2.5,
            'hello',
            {'type': 'ValueRef', 'value': '0'},
            {'type': 'ValueRef', 'value': '1'},
            {'type': 'ValueRef', 'value': '2'},
            {'type': 'ValueRef', 'value': '3'},
            {'type': 'ValueRef', 'value': '5'},
            {'type': 'ValueRef', 'value': '4'},
            {'type': 'ValueRef', 'value': '6'}
        ]]
    ],
    'value': {'type': 'ValueRef', 'value': '7'}
}
