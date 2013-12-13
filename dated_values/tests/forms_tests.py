"""Tests for the forms of the dated_values app."""
from django.test import TestCase
from django.utils.timezone import now

from django_libs.tests.factories import UserFactory

from ..forms import ValueForm
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
        form = ValueForm(self.user, now(), data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))
        form.save()
        self.assertEqual(DatedValue.objects.count(), 1, msg=(
            'After calling save, there are not the correct amount of dated'
            ' values in the database.'))

        value = DatedValue.objects.get()
        form = ValueForm(self.user, now(), instance=value, data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 1, msg=(
            'After calling save with an instance, there was not the correct'
            ' amount of dated values in the database.'))

        # Tests for not creating and deleting objects
        data = {'value': ''}
        form = ValueForm(self.user, now(), instance=value, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form with instance should be valid with the blank value.'
            ' Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 0, msg=(
            'After calling save with an empty value and an instance, the form'
            ' should have deleted that instance.'))

        data = {'value': ''}
        form = ValueForm(self.user, now(), data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid even with the value being blank.'
            ' Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(DatedValue.objects.count(), 0, msg=(
            'After calling save, there are not the correct amount of dated'
            ' values in the database.'))
