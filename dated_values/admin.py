"""Admin classes for the dated_values app."""
from django.contrib import admin

from .models import DatedValue, DatedValueType


admin.site.register(DatedValue)
admin.site.register(DatedValueType)
