# coding=utf-8
import datetime
from nekbot import _

__author__ = 'nekmo'

# TIME_TIMES = {'d': 3600 * 24, 'h': 3600, 'm': 60, 's': 1}
# HUMAN_TIMES = {
# 's': (_('second'), _('seconds')),
# 'm': (_('minute'), _('minutes')),
# 'h': (_('hour'), _('hours')),
# 'd': (_('day'), _('days')),
# }

MAGNITUDES = {
    'days': (_("day"), _("days")),
    'hours': (_("hour"), _("hours")),
    'minutes': (_("minute"), _("minutes")),
    'seconds': (_("second"), _("seconds")),
}


def human_join(list, and_='and', sep=', '):
    if len(list) == 1:
        return list[0]
    return '%s %s %s' % (sep.join(list[:-1]), and_, list[-1])


def strdelta(delta, join_str=', '):
    days, rem = divmod(delta.total_seconds(), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    if seconds < 1: seconds = 1
    locals_ = locals()
    magnitudes_str = []
    for magnitude in ('days', 'hours', 'minutes', 'seconds'):
        value = locals_[magnitude]
        if not value:
            continue
        magnitudes_str.append('%i %s' % (value, MAGNITUDES[magnitude][1] if value > 1
                                                else MAGNITUDES[magnitude][1]))
    eta_str = join_str.join(magnitudes_str)
    return eta_str