import inspect, json, getpass, os.path, base64, StringIO, re, warnings
import requests
from PIL import Image

from indicoio import JSON_HEADERS
from indicoio import config

B64_PATTERN = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)")


def api_handler(arg, cloud, api, batch=False, api_key=None, **kwargs):
    data = {'data': arg}
    data.update(**kwargs)
    json_data = json.dumps(data)
    if not cloud:
        cloud=config.cloud

    if cloud:
        host = "%s.indico.domains" % cloud
    else:
        # default to indico public cloud
        host = config.PUBLIC_API_HOST

    if not api_key:
        api_key = config.api_key

    url = config.url_protocol + "//%s/%s" % (host, api)
    url = url + "/batch" if batch else url
    url += "?key=%s" % api_key


    response = requests.post(url, data=json_data, headers=JSON_HEADERS)
    if response.status_code == 503 and cloud != None:
        raise Exception("Private cloud '%s' does not include api '%s'" % (cloud, api))

    json_results = response.json()
    results = json_results.get('results', False)
    if results is False:
        error = json_results.get('error')
        raise ValueError(error)
    return results


class TypeCheck(object):
    """
    Decorator that performs a typecheck on the input to a function
    """
    def __init__(self, accepted_structures, arg_name):
        """
        When initialized, include list of accepted datatypes and the
        arg_name to enforce the check on. Can totally be daisy-chained.
        """
        self.accepted_structures = accepted_structures
        self.is_accepted = lambda x: type(x) in accepted_structures
        self.arg_name = arg_name

    def __call__(self, fn):
        def check_args(*args, **kwargs):
            arg_dict = dict(zip(inspect.getargspec(fn).args, args))
            full_args = dict(arg_dict.items() + kwargs.items())
            if not self.is_accepted(full_args[self.arg_name]):
                raise DataStructureException(
                    fn,
                    full_args[self.arg_name],
                    self.accepted_structures
                )
            return fn(*args, **kwargs)
        return check_args


class DataStructureException(Exception):
    """
    If a non-accepted datastructure is passed, throws an exception
    """
    def __init__(self, callback, passed_structure, accepted_structures):
        self.callback = callback.__name__
        self.structure = str(type(passed_structure))
        self.accepted = [str(structure) for structure in accepted_structures]

    def __str__(self):
        return """
        function %s does not accept %s, accepted types are: %s
        """ % (self.callback, self.structure, str(self.accepted))


def image_preprocess(image, size=(48,48), batch=False):
    """
    Takes an image and prepares it for sending to the api including
    resizing and image data/structure standardizing.
    """
    if batch:
        return [image_preprocess(img, batch=False) for img in image]

    if isinstance(image, basestring):
        b64_str = re.sub('^data:image/.+;base64,', '', image)
        if os.path.isfile(image):
            # check type of element
            outImage = Image.open(image)
        elif B64_PATTERN.match(b64_str) is not None:
            return b64_str
        else:
            raise ValueError("Snose tring provided must be a valid filepath or base64 encoded string")

    elif isinstance(image, list): # image passed in is a list and not np.array
        warnings.warn(
            "Input as lists of pixels will be deprecated in the next major update",
            DeprecationWarning
        )
        outImage = process_list_image(image)
    elif type(image).__name__ == "ndarray": # image is from numpy/scipy
        out_image = Image.fromarray(image)
    else:
        raise ValueError("Image must be a filepath, base64 encoded string, or a numpy array")

    # image resizing
    outImage = outImage.resize(size)

    # convert to base64
    temp_output = StringIO.StringIO()
    outImage.save(temp_output, format='PNG')
    temp_output.seek(0)
    output_s = temp_output.read()

    return base64.b64encode(output_s)


def get_list_dimensions(_list):
    """
    Takes a nested list and returns the size of each dimension followed
    by the element type in the list
    """
    if isinstance(_list, list) or isinstance(_list, tuple):
        return [len(_list)] + get_list_dimensions(_list[0])
    return []


def get_element_type(_list, dimens):
    """
    Given the dimensions of a nested list and the list, returns the type of the
    elements in the inner list.
    """
    elem = _list
    for _ in xrange(len(dimens)):
        elem = elem[0]
    return type(elem)


def process_list_image(_list):
    """
    Processes list to be [[(int, int, int), ...]]
    """
    # Check if list is empty
    if not _list:
        return _list

    dimens = get_list_dimensions(_list)
    data_type = get_element_type(_list, dimens)

    seq_obj = []

    outImage = Image.new("RGB", (dimens[0], dimens[1]))
    for i in xrange(dimens[0]):
        for j in xrange(dimens[1]):
            elem = _list[i][j]
            if len(dimens) >= 3:
                #RGB(A)
                if data_type == float:
                    seq_obj.append((int(elem[0] * 255), int(elem[1] * 255), int(elem[2] * 255)))
                else:
                    seq_obj.append(elem[0:3])
            elif data_type == float:
                #Grayscale 0 - 1.0f
                seq_obj.append((int(elem * 255), ) * 3)
            else:
                #Grayscale 0 - 255
                seq_obj.append((elem, ) * 3)

    #Needs to be 0 - 255 in flattened list of (R, G, B)
    outImage.putdata(data = seq_obj)

    return outImage


def is_url(data, batch=False):
    if batch and isinstance(data[0], basestring):
        return True
    if not batch and isinstance(data, basestring):
        return True
    return False
