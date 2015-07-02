def say_hallo(name=None):
    """
    Gentle salute.
    @param name: Name of the guest.
    @type name: str
    @return: A string containing the salute to the guest.
    """
    s = 'Hallo ' + str(name) + '!' if name is not None else 'Hallo!'
    return s
