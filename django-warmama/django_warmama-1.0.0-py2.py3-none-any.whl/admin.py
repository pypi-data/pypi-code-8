from django.apps import apps
from django.contrib import admin

warmama = apps.get_app_config('warmama')

for model_name, model in warmama.models.items():
    admin.site.register(model)
