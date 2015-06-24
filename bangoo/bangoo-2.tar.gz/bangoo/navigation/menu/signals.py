from django.dispatch import Signal

menu_changed = Signal(providing_args=['menu', 'old_parent', 'new_parent'])
