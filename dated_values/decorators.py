"""Decorators for the dated_values app."""
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def permission_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                        login_url=None, test_to_pass=None):  # pragma: nocover
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.

    Customization based off the login_required decorator. Only difference is
    the possibility to pass different test functions (`test_to_pass`).

    """
    actual_decorator = user_passes_test(
        test_to_pass,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
