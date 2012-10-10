from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from sitemaps import StaticSitemap


# Enable the admin
admin.autodiscover()


sitemaps = {
    'static': StaticSitemap,
}


urlpatterns = patterns('',
    # XML Sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', { 
        'sitemaps': sitemaps }),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Robots.txt file
    url(r'^robots.txt$', include('django_robots.urls')),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^404/$', TemplateView.as_view(template_name="404.html")),
        url(r'^500/$', TemplateView.as_view(template_name="500.html")),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )