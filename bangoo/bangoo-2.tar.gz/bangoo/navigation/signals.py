from django.dispatch import Signal

menu_created = Signal(providing_args=['menu', 'user'])