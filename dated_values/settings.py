"""Settings and defaults for the dated_values app."""
from django.conf import settings

ACCESS_ALLOWED = getattr(settings, 'DATED_VAUES_ACCESS_ALLOWED',
                         lambda user: user.is_staff)
DISPLAYED_ITEMS = getattr(settings, 'DATED_VAUES_DISPLAYED_ITEMS', 14)
DATE_FORMAT = getattr(settings, 'DATED_VAUES_DATE_FORMAT', '%d-%m-%Y')
