__author__ = 'nekmo'

def human_join(list, and_='and', sep=', '):
    if len(list) == 1:
        return list[0]
    return '%s %s %s' % (sep.join(list[:-1]), and_, list[-1])

def long_message(message, newlines=1, length=140):
    if not isinstance(message, (str, unicode)):
        message = str(message)
    if len(message) > length:
        return True
    if len(message.split('\n')) - 1 > newlines:
        return True
    return False