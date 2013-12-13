"""Forms of the dated_values app."""
from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import DatedValue, DatedValueType


class ValueForm(forms.ModelForm):
    """Form to handle one single DatedValue instance."""

    def __init__(self, obj, date, *args, **kwargs):
        super(ValueForm, self).__init__(*args, **kwargs)
        self.instance.type = DatedValueType.objects.get(
            ctype=ContentType.objects.get_for_model(obj.__class__))
        self.instance.date = date
        self.instance.object_id = obj.id

    class Meta:
        fields = ['value', ]
        model = DatedValue
