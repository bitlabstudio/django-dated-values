"""Tests for the forms of the dated_values app."""
from django.test import TestCase
from django.utils.timezone import now

from django_libs.tests.factories import UserFactory

from ..forms import ValueForm, ValueFormset
from ..models import DatedValue
from .factories import DatedValueTypeFactory


class ValueFormTestCase(TestCase):
    """Tests for the most basic ValueForm."""
    longMessage = True

    def setUp(self):
        self.data = {'value': '2.22'}
        self.user = UserFactory()
        self.type = DatedValueTypeFactory()

    def test_form(self):
        # Tests for creating objects
        form = ValueForm(self.user, now(), self.type, data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))
        form.save()
        self.assertEqual(DatedValue.objects.count(), 1, msg=(
            'After calling save, there are not the correct amount of dated'
            ' values in the database.'))

        value = DatedValue.objects.get()
        form = ValueForm(self.user, now(), self.type, instance=value,
                         data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 1, msg=(
            'After calling save with an instance, there was not the correct'
            ' amount of dated values in the database.'))

        # Tests for not creating and deleting objects
        data = {'value': ''}
        form = ValueForm(self.user, now(), self.type, instance=value,
                         data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form with instance should be valid with the blank value.'
            ' Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 0, msg=(
            'After calling save with an empty value and an instance, the form'
            ' should have deleted that instance.'))

        data = {'value': ''}
        form = ValueForm(self.user, now(), self.type, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid even with the value being blank.'
            ' Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 0, msg=(
            'After calling save, there are not the correct amount of dated'
            ' values in the database.'))


class ValueFormsetTestCase(TestCase):
    """Tests for the ValueFormset formset class."""
    longMessage = True

    def setUp(self):
        self.data = {
            'form-TOTAL_FORMS': u'0',
            'form-INITIAL_FORMS': u'0',
            'form-0-value': '0.22',
            'form-1-value': '1.22',
            'form-2-value': '2.22',
            'form-3-value': '3.22',
            'form-4-value': '4.22',
            'form-5-value': '5.22',
            'form-6-value': '6.22',
        }
        self.user = UserFactory()
        self.type = DatedValueTypeFactory()

    def test_form(self):
        # Tests for creating objects
        form = ValueFormset(self.user, now(), 7, self.type, data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))
        form.save()
        self.assertEqual(DatedValue.objects.count(), 7, msg=(
            'After calling save, there are not the correct amount of dated'
            ' values in the database.'))

        form = ValueFormset(self.user, now(), 7, self.type, data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 7, msg=(
            'After calling save on the form, where we have instances in the'
            ' database, there should still be the same instances in the'
            ' database.'))

        # Tests for not creating and deleting objects
        data = self.data.copy()
        data.update({'form-0-value': '', 'form-4-value': ''})
        form = ValueFormset(self.user, now(), 7, self.type, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid with the blank values.'
            ' Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 5, msg=(
            'After calling save on the formset with 2 empty values and'
            ' persistent values in th database, there should be a decreased'
            ' amount of values in the database.'))

        form = ValueFormset(self.user, now(), 7, self.type, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid even with some values being blank.'
            ' Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 5, msg=(
            'When we call save again with the same data, there should be'
            ' the same amount of values in the database.'))
