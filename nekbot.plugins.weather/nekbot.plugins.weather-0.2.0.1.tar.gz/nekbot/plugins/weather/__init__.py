# coding=utf-8
import datetime
import forecastio
from nekbot import settings
from nekbot.core.exceptions import InvalidArgument
from nekbot.plugins.geo import place_coord

__author__ = 'Nekmo'

from nekbot.core.commands import command

DATETIME_PATTERN = '%d/%m/%Y %H:%M'
DATE_PATTERN = '%d/%m/%Y'

INFO = ('summary', 'temperature', 'temperatureMin', 'temperatureMax')
EXTRA_INFO = INFO + ('apparentTemperature', 'humidity', 'windSpeed')

FORMATS = {
    'temperature': u'%.1fºc',
    'temperatureMin': u'%.1fºc min.',
    'temperatureMax': u'%.1fºc max.',
    'apparentTemperature': u'%.1fºc RealFeel',
    'humidity': u'%i%% humid.',
    'windSpeed': u'wind %.2fkm/h',
}

MOMENTS = {
    'now': lambda x: x.currently(),
    'today': lambda x: x.daily().data[0],
    'tomorrow': lambda x: x.daily().data[1],
    'after-tomorrow': lambda x: x.daily().data[2],
    # 'yesterday': lambda x: x,
}

MOMENTS['n'] = MOMENTS['now']
MOMENTS['ty'] = MOMENTS['today']
MOMENTS['tw'] = MOMENTS['tomorrow']
MOMENTS['aw'] = MOMENTS['after-tomorrow']
# MOMENTS['y'] = MOMENTS['yesterday']


def format_weather(fc, info=INFO, formats=FORMATS):
    return ' '.join([formats.get(key, '%s') % fc.d[key] for key in info if key in fc.d])


def moment(text):
    if not text:
        return text
    elif text in MOMENTS:
        return MOMENTS[text]
    dt = None
    try:
        dt = datetime.datetime.strptime(text, DATETIME_PATTERN)
    except ValueError:
        pass
    try:
        dt = datetime.datetime.strptime(text, DATE_PATTERN)
    except ValueError:
        pass
    if dt is None:
        raise InvalidArgument('Argument is not a moment or datetime.', text)
    return dt


@command('weather', place_coord, moment=moment)
def weather(msg, coord, moment=None):
    try:
        fc = forecastio.load_forecast(settings.FORECAST_KEY, coord[0], coord[1],
                                      time=moment if isinstance(moment, datetime.datetime) else None)
    except ValueError as e:
        return 'Ops! No data for this place or moment: %s' % e.message
    if not moment:
        return u'Now: %s ⚫ Tomorrow: %s' % (format_weather(fc.currently()), format_weather(fc.daily().data[0]))
    elif isinstance(moment, datetime.datetime):
        return u'%s' % format_weather(fc.currently(), EXTRA_INFO)
    elif hasattr(moment, '__call__'):
        return u'%s' % format_weather(moment(fc), EXTRA_INFO)
    else:
        raise NotImplementedError