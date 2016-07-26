from django.conf.urls import url
from . import views
# from .feeds import UpdateFeed

urlpatterns = [
    url(r'^$',
        views.SiteHome.as_view()),

    url(r'^e/(?P<slug>.+)/(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='events.event_detail'),

    url(r'^u/(?P<date>\d{4}-\d{2}-\d{2})/$',
        views.WeeklyUpdate.as_view(),
        name='events.weekly_update'),

    url(r'^u/(?P<date>\d{4}-\d{2}-\d{2})/email-preview/$',
        views.WeeklyUpdateEmailPreview.as_view(),
        name='events.weekly_update_email_preview'),

    # url(r'feed/rss/$', UpdateFeed()),
]
