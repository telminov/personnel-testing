from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.template.base import add_to_builtins

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^', include('auth2.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grppll/', include('grappelli.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

