from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.conf import settings


class PermissionRequiredTestCase(TestCase):
    """Test PermissionRequired mixin functionality."""

    def setUp(self):
        # create a test permission
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename='test_permission',
            content_type=content_type,
            name='Test permission'
        )

        # create a user with permission
        perm_user = User.objects.create_user(
            'perm', 'perm@example.com', 'pass')
        perm_user.user_permissions.add(permission)

        # and one without
        noperm_user = User.objects.create_user(
            'noperm', 'noperm@example.com', 'pass')

        # anonymous client
        self.anonymous = Client()

        # authenticated client with perm
        self.authorized = Client()
        self.authorized.login(username='perm', password='pass')

        # authenticated client without perm
        self.unauthorized = Client()
        self.unauthorized.login(username='noperm', password='pass')

        self.url = reverse('test_permission_required')

    def test_anonymous_user_denied(self):
        response = self.anonymous.get(self.url)
        self.assertEquals(response.status_code, 403)

    def test_unauthorized_user_denied(self):
        response = self.unauthorized.get(self.url)
        self.assertEquals(response.status_code, 403)

    def test_authorized_user_ok(self):
        response = self.authorized.get(self.url)
        self.assertEquals(response.status_code, 200)
