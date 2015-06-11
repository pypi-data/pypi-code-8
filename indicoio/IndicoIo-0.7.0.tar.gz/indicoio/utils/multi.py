from indicoio.config import TEXT_APIS, IMAGE_APIS, API_NAMES
from indicoio.utils.api import api_handler
from indicoio.utils.image import image_preprocess
from indicoio.utils.errors import IndicoError


CLIENT_SERVER_MAP = dict((api, api.strip().replace("_", "").lower()) for api in API_NAMES)
SERVER_CLIENT_MAP = dict((v, k) for k, v in CLIENT_SERVER_MAP.iteritems())

def multi(data, type, apis, available, batch=False, **kwargs):
    """
    Helper to make multi requests of different types.

    :param data: data to be sent in JSON.
    :param type: String type of API request
    :param apis: List of apis to use.
    :param apis: List of apis available for use.
    :type data: str or image
    :type type: str or unicode
    :type apis: list of str
    :type available: list of str
    :rtype: Dictionary of api responses
    """
    # Client side api name checking - strictly only accept func name api
    invalid_apis = [api for api in apis if api not in available]
    if invalid_apis:
        raise IndicoError("%s are not valid %s APIs. Please reference the available APIs below:\n%s"
                            % (", ".join(invalid_apis), type, ", ".join(available))
                        )
    # Convert client api names to server names before sending request
    apis = map(CLIENT_SERVER_MAP.get, apis)
    result = api_handler(data, url_params = {"apis":apis, "batch":batch}, **kwargs)
    return handle_response(result)

def handle_response(result):
    # Parse out the results to a dicionary of api: result
    return dict((SERVER_CLIENT_MAP[api], parsed_response(api, res))
        for api, res in result.iteritems())


def predict_text(input_text, apis=TEXT_APIS, cloud=None, batch=False, api_key=None, **kwargs):
    """
    Given input text, returns the results of specified text apis. Possible apis
    include: [ 'text_tags', 'political', 'sentiment', 'language' ]

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> results = indicoio.text(data = text, apis = ["language", "sentiment"])
       >>> language_results = results["langauge"]
       >>> sentiment_results = results["sentiment"]

    :param text: The text to be analyzed.
    :param apis: List of apis to use.
    :type text: str or unicode
    :type apis: list of str
    :rtype: Dictionary of api responses
    """

    return multi(
        api="apis",
        data=input_text,
        type="text",
        available = TEXT_APIS,
        cloud=cloud,
        batch=batch,
        api_key=api_key,
        apis=apis,
        **kwargs)


def predict_image(image, apis=IMAGE_APIS, cloud=None, batch=False, api_key=None, **kwargs):
    """
    Given input image, returns the results of specified image apis. Possible apis
    include: ['fer', 'facial_features', 'image_features']

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> face = np.zeros((48,48)).tolist()
       >>> results = indicoio.image(image = face, apis = ["fer", "facial_features"])
       >>> fer = results["fer"]
       >>> facial_features = results["facial_features"]

    :param text: The text to be analyzed.
    :param apis: List of apis to use.
    :type text: str or unicode
    :type apis: list of str
    :rtype: Dictionary of api responses
    """

    return multi(
        api="apis",
        data=image_preprocess(image, batch=batch),
        type="image",
        available=IMAGE_APIS,
        cloud=cloud,
        batch=batch,
        api_key=api_key,
        apis=apis,
        **kwargs)

def parsed_response(api, response):
    result = response.get('results', False)
    if result:
        return result
    raise IndicoError(
        "Sorry, the %s API returned an unexpected response.\n\t%s"
        % (api, response.get('error', ""))
    )
