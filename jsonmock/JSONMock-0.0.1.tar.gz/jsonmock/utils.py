__author__ = 'anass'


def path_to_property(obj, props, id_tag='id'):
    """ Get the property value from a path"""
    if isinstance(obj, list):
        # If it is a list it means we need the id to return the value
        # add if value equal nan ==> no resource found
        if len(props) is 1:
            res = [o for o in obj if o.get(id_tag).__eq__(props[0])]
            if not len(res):
                # no resource found
                return
            return props[0], res[0]
        return props[0], [o for o in obj]
        #return path_to_property([o for o in obj if o.get(id_tag).__eq__(props[0])][0], props[1:])   # filter ID
    if len(props) == 1:
        return props[0], obj.get(props[0])
    return path_to_property(obj.get(props[0]), props[1:])


def dict_to_json(obj):
    json = {}
    for key in obj.keys():
        for value in obj.getlist(key):
            json[key] = value
    return json


