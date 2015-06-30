import math


class BytesType(float):

    @property
    def human(self):
        if not self:
            return '0B'
        value = self
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if value >= prefix[s]:
                value = value / prefix[s]
                return '%.1f%s' % (value, s)
        return '%sB' % value


class PercType(float):

    @property
    def human(self):
        return '%.2f%%' % self


class TimeType(float):

    @property
    def human(self):
        d, h, m, s = 0, 0, 0, 0
        m = math.floor(self / 60)
        s = self % 60
        if m > 59:
            h = math.floor(m / 60)
            m = m % 60
        if h > 24:
            d = math.floor(h / 24)
            h = h % 24

        result = ['P']
        if d:
            result.append('%sD' % d)
        result = ['T']
        if h:
            result.append('%02dH' % h)
        if m:
            result.append('%02dM' % m)
        if s:
            result.append('%02dS' % int(s))
        return ''.join(result)


def mark(obj, type=None):
    if type in ('bytes',):
        return BytesType(obj)
    if type in ('percentage',):
        return PercType(obj)
    if type in ('duration',):
        return TimeType(obj)
    return obj
