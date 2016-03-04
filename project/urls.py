from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^', include('auth2.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^select2/', include('django_select2.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

