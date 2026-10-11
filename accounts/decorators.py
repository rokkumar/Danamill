from django.contrib.auth.decorators import user_passes_test


def staff_required(view_func):
    """
    Only staff users can access the view.
    Non-staff gets redirected to login.
    """
    decorated = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/login/',
    )(view_func)
    return decorated