
from django.conf import settings

from django.conf.urls import patterns, include, url
from django.contrib import admin

from mezzanine.core.views import direct_to_template

admin.autodiscover()

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    url(r'^auth/', include('allauth.urls')),
    url(r"^account/", include("account.urls")),
    url(r"^cart/", include("cart.urls")),
    url(r'^admin/salmonella/', include('salmonella.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
)

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"

# mezzanine last urls handling, put it on bottom
urlpatterns += patterns('',
    ("^", include("mezzanine.urls")),
)
