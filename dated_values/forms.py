"""Forms of the dated_values app."""
from dateutil.relativedelta import relativedelta
from django import forms

from .models import DatedValue


class ValueForm(forms.ModelForm):
    """Form to handle one single DatedValue instance."""

    def __init__(self, obj, date, valuetype, *args, **kwargs):
        """
        :param obj: An object, that has values attached.
        :param date: A datetime date.
        :param valuetype: The DatedValueType, we are working on.

        """
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


class ValueFormset(forms.models.modelformset_factory(DatedValue, ValueForm)):
    """Formset to for the ValueForm form."""

    def __init__(self, obj, date, length, valuetype, *args, **kwargs):
        """
        :param obj: An object, that has values attached.
        :param date: A datetime date.
        :param length: The amount of ValueFormsets to display.
        :param valuetype: The DatedValueType, we are working on.

        """
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


class MultiTypeValueFormset(forms.formsets.formset_factory(ValueFormset)):
    """A formset, that allows to add multiple ValueFormset in one go."""
    def __init__(self, obj, date, length, valuetypes, *args, **kwargs):
        """
        :param obj: An object, that has values attached.
        :param date: A datetime date.
        :param length: The amount of ValueFormsets to display.
        :param valuetypes: A list of DatedValueTypes

        """
        self.extra = len(valuetypes)
        super(MultiTypeValueFormset, self).__init__(*args, **kwargs)
        for valuetype in valuetypes:
            self.formset_prefix = '{0}_{1}'.format(
                valuetype.slug, str(valuetype.id))
            formset = ValueFormset(obj, date, length, valuetype,
                                   prefix=self.formset_prefix,
                                   data=kwargs.get('data'))
            self.forms.append(formset)

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors.

        since we tricked the form again to also process extra forms and empty
        ones, we need to use self.extra and not total_form_count as the range
        max below.

        """
        self._errors = []
        for i in range(0, self.extra):
            form = self.forms[i]
            self._errors.append(form.errors)

    def save(self):
        return_val = []
        for form in self.forms:
            return_val.append(form.save())
