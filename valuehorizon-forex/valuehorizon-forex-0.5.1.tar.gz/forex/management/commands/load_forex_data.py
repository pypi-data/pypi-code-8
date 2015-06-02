# encoding: utf-8

# Import Django libraries
from django.core.management.base import LabelCommand# BaseCommand, CommandError
from django.utils.termcolors import colorize

# Import project libraries
from forex.models import Currency

# Import other libraries

    
class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Load the latest forex Currency data.'

    def handle(self, **options):
        
        if Currency.objects.count() > 0:
            print colorize("You already have Currency objects in the database\n \
                Try running ./manage.py maintain_forex_data to update your data instead.", 
                fg="red")
        
        