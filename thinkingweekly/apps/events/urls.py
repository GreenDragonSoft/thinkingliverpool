from django.conf.urls import url
from . import views
# from .feeds import UpdateFeed

DATE_PATTERN = '\d{4}-\d{2}-\d{2}'

urlpatterns = [
    url(r'^$',
        views.SiteHome.as_view()),

    url(r'^e/(?P<slug>.+)/(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='events.event_detail'),

    url(r'^u/(?P<date>' + DATE_PATTERN + ')/email-preview/$',
        views.UpdateEmailPreview.as_view(),
        name='events.update_email_preview'),

    # url(r'feed/rss/$', UpdateFeed()),
]
