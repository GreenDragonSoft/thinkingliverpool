from django.conf.urls import url
from . import views
# from .feeds import UpdateFeed

DATE_PATTERN = '\d{4}-\d{2}-\d{2}'

urlpatterns = [
    url(r'^$',
        views.SiteHome.as_view(),
        name='site_home'),

    url(r'^about/$',
        views.About.as_view(),
        name='events.about'),

    url(r'^whats-on-in-liverpool/$',
        views.EventList.as_view(),
        name='events.event_list'),

    url(r'^events-in-liverpool/past-events/$',
        views.PastUpdatesList.as_view(),
        name='events.past_updates'),

    url(r'^events-in-liverpool/(?P<slug>.+)/$',
        views.VenueEventList.as_view(),
        name='events.venue_event_list'),

    url(r'^events-in-liverpool/(?P<date>' + DATE_PATTERN + ')/$',
        views.WeeklyUpdateEventList.as_view(),
        name='events.weekly_update_event_list'),

    url(r'^e/(?P<slug>.+)/(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='events.event_detail'),

    url(r'^u/(?P<date>' + DATE_PATTERN + ')/email-preview/$',
        views.UpdateEmailPreview.as_view(),
        name='events.update_email_preview'),

    # url(r'feed/rss/$', UpdateFeed()),
]
