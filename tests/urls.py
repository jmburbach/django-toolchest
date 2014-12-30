from django.conf.urls import include, patterns, url

from .views import (
    LoginRequiredRedirectView,
    LoginRequiredNoRedirectView,
    PermissionRequiredView
)

urlpatterns = patterns('',
    url(r'^tests/login-required-redirect/$',
        LoginRequiredRedirectView.as_view(),
        name='test_login_required_redirect'
    ),
    url(r'^tests/login-required-no-redirect/$',
        LoginRequiredNoRedirectView.as_view(),
        name='test_login_required_no_redirect'
    ),
    url(r'^tests/permission-required/$',
        PermissionRequiredView.as_view(),
        name='test_permission_required'
    ),
    url(r'^accounts/', include('django.contrib.auth.urls'))
)
