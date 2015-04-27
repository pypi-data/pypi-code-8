"""
Definition for the get_historical_djia Django management command
"""

import datetime
import logging

from django.core.management.base import BaseCommand, CommandError

from geohashing.utils import get_historical_djia_openings
from geohashing.models import Day


ONE_DAY = datetime.timedelta(days=1)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command for populating database from historical DJIA data
    """
    help = 'Retrieve and import historical DJIA opening data'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s', '--start',
            help='First date to retrieve, in YYYY-MM-DD format',
            type=str
        )
        parser.add_argument(
            '-e', '--end',
            help='Last date to retrieve, in YYYY-MM-DD format',
            type=str
        )

    def handle(self, *args, **options):
        start = options.get('start')
        end = options.get('end')
        if start is not None:
            try:
                start_y, start_m, start_d = tuple(int(s) for s in start.split('-'))
                start = datetime.date(start_y, start_m, start_d)
            except (TypeError, ValueError):
                raise CommandError(
                    '{} not parseable as a datetime.date'.format(start)
                )
        if end is not None:
            try:
                end_y, end_m, end_d = tuple(int(s) for s in end.split('-'))
                end = datetime.date(end_y, end_m, end_d)
            except (TypeError, ValueError):
                raise CommandError(
                    '{} not parseable as a datetime.date'.format(end)
                )
        openings = get_historical_djia_openings(start, end)

        # This won't be performant when adding large amounts of data
        # (death by round trip). A better 2nd pass solution would be to
        # separate out the handling of updates and then use bulk_create
        # for new object creation. Additionally, this should be updated
        # to create Day rows for future dates we can safely extrapolate
        # (e.g. the Saturday and Sunday geohashes once we know Friday's
        # DJIA open).
        for geohash_date, djia_value in openings.items():
            previous_day = geohash_date - ONE_DAY
            if previous_day in openings:
                adj_djia_value = openings[previous_day]
                logger.info(
                    'Saving geohash data for date %s with 30w adjustment',
                    str(geohash_date)
                )
                day, created = Day.objects.update_or_create(
                    geohash_date=geohash_date,
                    djia_open=djia_value,
                    djia_open_30w_adj=adj_djia_value
                )
                logger.info(
                    'New objected created for %s: %s',
                    str(geohash_date),
                    str(created)
                )
            else:
                logger.info(
                    'Saving geohash data for date %s without 30w adjustment',
                    str(geohash_date)
                )
                day, created = Day.objects.update_or_create(
                    geohash_date=geohash_date,
                    djia_open=djia_value
                )
                logger.info(
                    'New object created %s: %s',
                    str(geohash_date),
                    str(created)
                )
