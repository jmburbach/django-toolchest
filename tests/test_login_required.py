from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings


class LoginRequiredTestCase(TestCase):
    """Test LoginRequired mixin functionality."""

    def setUp(self):
        User.objects.create_user('test', 'test@example.com', 'pass')

        self.anonymous = Client()

        self.authenticated = Client()
        self.authenticated.login(username='test', password='pass')

    def test_login_required_redirect(self):
        url = reverse('test_login_required_redirect')

        # anonymous client should get redirected to login
        response = self.anonymous.get(url)
        self.assertRedirects(
            response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # and authenticated should be ok
        response = self.authenticated.get(url)
        self.assertEquals(response.status_code, 200)

    def test_login_required_no_redirect(self):
        url = reverse('test_login_required_no_redirect')

        # anonymous should get forbidden 403
        response = self.anonymous.get(url)
        self.assertEquals(response.status_code, 403)

        # and authenticated should be ok
        response = self.authenticated.get(url)
        self.assertEquals(response.status_code, 200)
