import django.dispatch

payment_received = django.dispatch.Signal(providing_args=['amount', 'transaction_id'])

payment_cancelled = django.dispatch.Signal(providing_args=['transaction_id'])