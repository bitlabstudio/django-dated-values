"""Forms of the dated_values app."""
from dateutil.relativedelta import relativedelta
from django import forms
from django.forms.models import modelformset_factory

from .models import DatedValue


class ValueForm(forms.ModelForm):
    """Form to handle one single DatedValue instance."""

    def __init__(self, obj, date, valuetype, *args, **kwargs):
        super(ValueForm, self).__init__(*args, **kwargs)
        self.instance.type = valuetype
        self.instance.date = date
        self.instance.object_id = obj.id
        self.fields['value'].required = False
        self.allow_empty = True

    def save(self, **kwargs):
        if self.instance.value:
            return super(ValueForm, self).save(**kwargs)
        elif self.instance.id:
            self.instance.delete()
            return None

    class Meta:
        fields = ['value', ]
        model = DatedValue


class ValueFormset(modelformset_factory(DatedValue, ValueForm)):
    """Formset to for the ValueForm form."""

    def __init__(self, obj, date, length, valuetype, *args, **kwargs):
        self.extra = length
        super(ValueFormset, self).__init__(*args, **kwargs)
        values = DatedValue.objects.filter(
            type=valuetype, date__gte=date,
            date__lt=date + relativedelta(days=length))
        # we assign the forms ourselves, because django would always try to
        # create the first set of forms from the queryset and then append the
        # extra empty ones. We though want to mix create and update forms in a
        # variable order.
        for days in range(0, length):
            form_data = {'value': self.data.get('{0}-{1}-value'.format(
                self.prefix, days))}
            value_date = date + relativedelta(days=days)
            try:
                instance = values.get(date=value_date)
            except DatedValue.DoesNotExist:
                instance = None
            form = ValueForm(obj, value_date, valuetype, instance=instance,
                             data=form_data)
            self.forms.append(form)
