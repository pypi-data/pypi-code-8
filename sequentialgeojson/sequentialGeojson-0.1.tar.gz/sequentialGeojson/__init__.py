# -*- coding: utf-8 -*-
"""
sequentialGeojson

This module provides a generator interface to geojson files consisting of a
feature collection and returns its content feature-by-feature as an iterator.
This helps reading huge files without blocking the system.
"""


def reader(file):
    """A generator class for providing an iterator object to iterate over each
    single geojson entry in a given feature collection geojson file.

    Parameters
    ----------
    file: file object
        a valid geojson file as file object containing a feature collection

    Returns
    -------
    jsonFeature: string
        with each iteration, one geojson feature is returned
    """
    textbuffer = ""         # used to detect the beginning of the feature array
    featuresFound = False   # whether the beginning of the features array was alredy passed
    insideFeature = False   # detect whether we are inside a feature already
    featureDepth = 0        # used for counting the level of brackets
    jsonFeature = ""        # chars that make up one geoJson feature
    i = 0
    while True:
        currentChar = file.read(1)
        i += 1
        if not currentChar:
            break

        if featuresFound is False:
            # first round, search for the position of the feature-array
            if len(textbuffer) < 10:
                textbuffer += currentChar
            else:
                textbuffer = textbuffer[1:] + currentChar

            if textbuffer.lower() in ['"features"', "'features'"]:
                # search for the bracket of the start of the features array
                while featuresFound is False:
                    currentChar = file.read(1)
                    i += 1
                    if currentChar == "[":
                        featuresFound = True
        # when we have already passed by the start of the features array
        else:
            # check if we still have to find the entry of a new feature
            if insideFeature is False:
                if currentChar == '{':
                    insideFeature = True
                    jsonFeature = currentChar
                elif currentChar == "]":
                    # end of features array
                    break
            else:
                # we have to collect chars until the end of the feature
                if featureDepth == 0 and currentChar == "}":
                    # the current feature has been found
                    jsonFeature += currentChar
                    insideFeature = False
                    yield jsonFeature
                    # yield "this is a feature"
                else:
                    if currentChar == "{":
                        featureDepth += 1
                    elif currentChar == "}":
                        featureDepth -= 1
                    jsonFeature += currentChar
    file.close()


if __name__ == '__main__':
    import io
    print( "Running tests ..." )

    #validFeatureCollection = 'testdata/vienna-bratislava_austria-admin.geojson'
    validFeatureCollection = io.StringIO("""{"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },"features": [{ "type": "Feature", "properties": { "osm_id": -3908.0, "name": null, "type": "water", "area": 545473.0 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 17.014256566618194, 48.153410160655881 ], [ 17.014938266803306, 48.155379656444566 ], [ 17.039831429581223, 48.149782472962386 ], [ 17.039792286093412, 48.149617098012797 ] ] ] } },{ "type": "Feature", "properties": { "osm_id": -779.0, "name": "Velké Čunovo", "type": "water", "area": 366164.0 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 17.171381041299888, 48.038607256201786 ], [ 17.173297228184396, 48.039979289932262 ], [ 17.175540896025858, 48.038291258452169 ], [ 17.17521467235434, 48.038144072232413 ] ] ] } },{ "type": "Feature", "properties": { "osm_id": -14574.0, "name": null, "type": "water", "area": 329179.0 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 16.791912251886313, 47.941364522715233 ], [ 16.796197583702789, 47.942117636715345 ], [ 16.793797677186145, 47.941396541585341 ], [ 16.793109355297553, 47.941284978454121 ] ] ] } },{ "type": "Feature", "properties": { "osm_id": -17709.0, "name": "Zlaté piesky", "type": "water", "area": 1180090.0 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 17.180960383160762, 48.183428941043466 ], [ 17.182910935848266, 48.183815262960714 ], [ 17.190358256817941, 48.183647038164018 ], [ 17.188335535944102, 48.182980341585591 ] ] ] } }]}""")
    testreader = reader(validFeatureCollection)
    # print len(list(reader))

    for i, readerdata in enumerate(testreader):
        print( "-"*13,"\n","Feature #", i, "\n","-"*13)
        print( readerdata )
