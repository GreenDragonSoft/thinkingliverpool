"""thinkingweekly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views import static

from django.contrib.sitemaps.views import sitemap

from thinkingweekly.apps.events.sitemap import (
    UpdateSitemap, VenueSitemap, MonthYearSitemap
)


# http://www.thinkingliverpool.com                   <-- upcoming events
# http://www.thinkingliverpool.com/ical              <-- upcoming events (ical)
#
# http://www.thinkingliverpool.com/e/ignite-whats-happening-5iwJyIPI/
# ^^ note that 5iwJyIPI is the created_at 20160714221816 in a new base

sitemaps = {
    'past_updates': UpdateSitemap,
    'venues': VenueSitemap,
    'month_year_pages': MonthYearSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('thinkingweekly.apps.events.urls')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps})

    # url(r'^_status/', include('thinkingweekly.apps.status.urls')),
    # url(r'^api/', include('thinkingweekly.apps.api.urls')),
]

# If filesystem-based-media is enable, add a URL and serve static files through
# Django (not for production!)

if settings.FILESYSTEM_BASED_MEDIA:
    urlpatterns += [
        url(
            r'^media-uploads/(?P<path>.*)$',
            static.serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        )
    ]
