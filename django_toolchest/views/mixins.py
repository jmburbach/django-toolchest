from django.http import HttpResponseForbidden
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class LoginRequired(object):
    """View mixin that allows one to easily check that user is logged in. When
    attribute `login_redirect' is True (the default), then will redirect to the
    login url if user is not logged in. If `login_redirect' attribute is set to
    False, then will return a HttpResponseForbidden (403) response instead. If
    this behavior is insufficient subclasses can instead override the
    `get_not_logged_in_response' method to perform custom handling and return
    an appropriate response.

    Log in checks are performed in the `dispatch' method of view. If your
    subclass will override the dispatch method then it is recommended that your
    dispatch method looks like the following:

        def dispatch(self, request, *args, **kwargs):
            logged_in, response = self.check_login()
            if not logged_in:
                return response

            YOUR CODE HERE

            return super(YourClass, self).dispatch(request, *args, **kwargs)

    This ensures that the login check happens BEFORE your code is run, rather
    than AFTER it."""
    login_checked = False
    login_redirect = True

    def dispatch(self, request,  *a, **k):
        logged_in, response = self.check_login()
        if not logged_in:
            return response
        return super(LoginRequired, self).dispatch(request, *a, **k)

    def get_login_redirect(self):
        """Return True if view should redirect to login url if user is not
        logged in, else False. Simply returns `login_redirect' by default."""
        return self.login_redirect

    def get_not_logged_in_response(self):
        """Return an appropriate response for a request from a user not logged
        in.

        By default this will return a redirect to login url if the
        `get_login_redirect' method returns True, or a 403 forbidden response
        if it returns False.

        This method can be overridden to perform custom handling, but should
        always return a http response."""
        if self.get_login_redirect():
            return redirect_to_login(self.request.get_full_path())
        return HttpResponseForbidden()

    def check_login(self):
        retval = (True, None)

        if self.login_checked:
            return retval

        self.login_checked = True

        logged_in = self.request.user.is_authenticated()
        if not logged_in:
            retval = (False, self.get_not_logged_in_response())

        return retval


class PermissionRequired(object):
    """View mixin to allow easily check for required permission. Just
    set the permission_required attribute or override the
    get_permission_required method to specify the required permission.

    Permission checks are performed in the `dispatch' method of view. If your
    subclass will override the dispatch method then it is recommended that your
    dispatch method looks like the following:

        def dispatch(self, request, *args, **kwargs):
            self.check_permission()

            YOUR CODE HERE

            return super(YourClass, self).dispatch(request, *args, **kwargs)

    This ensures that the perm check happens BEFORE your code is run, rather
    than AFTER it."""
    permission_checked = False
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        self.check_permission()
        return super(PermissionRequired, self).dispatch(
            request, *args, **kwargs)

    def get_permission_required(self):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                'You must set the permission_required attribute '
                'or override the get_permission_required method'
            )
        return self.permission_required

    def check_permission(self):
        if self.permission_checked:
            return

        self.permission_checked = True

        perm = self.get_permission_required()
        has_perm = self.request.user.has_perm(perm)

        if not has_perm:
            raise PermissionDenied
