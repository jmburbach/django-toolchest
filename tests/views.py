from django.views.generic.base import View
from django.http import HttpResponse

from django_toolchest.views.mixins import LoginRequired, PermissionRequired


class TestView(View):
    """Base test view that always returns ok."""

    def get(self, request):
        return HttpResponse()


class LoginRequiredRedirectView(LoginRequired, TestView):
    """View that requires a login and redirects to login url."""
    login_redirect=True


class LoginRequiredNoRedirectView(LoginRequired, TestView):
    """View that requires a login and does not redirect but instead
    returns a forbidden response."""
    login_redirect = False


class PermissionRequiredView(PermissionRequired, TestView):
    """View that requires a user have the 'test_permission' permission."""
    permission_required = 'auth.test_permission'
