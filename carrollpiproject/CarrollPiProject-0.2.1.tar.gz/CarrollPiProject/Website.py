import requests


def sendDataToWebsite(celsius, fahrenheit, dissolvedOxygen, school, username, password):
    """Sends Dissoloved oxygen and Temperature data to the website API: Requires the login token

    Args: \n
    :param celsius: the temperature in celsius \n
    :type celsius: str \n
    :param fahrenheit: the temperature in fahrenheit \n
    :type fahrenheit: str \n
    :param dissolvedOxygen: the dissolved oxygen \n
    :type dissolvedOxygen: str \n
    :param school: the location of the device \n
    :type school: str \n
    :param username: CarrollPiProject Username. \n
    :type username: str \n
    :param password: CarrollPiProject Password. \n
    :type password: str \n
    """
    body = {'celsius': celsius,
            'fahrenheit': fahrenheit,
            'dissolvedOxygen': dissolvedOxygen,
            'school': school,
            'username': username,
            'password': password}
    requests.post("http://www.carrollpiproject.com/dataApi", data=body)
