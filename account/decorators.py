from django.contrib.auth.decorators import user_passes_test


def superuser_required(func=None, redirect_field_name=None, login_url='account:no_permission'):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if func:
        return actual_decorator(func)
    return actual_decorator
