from django.conf.urls import url
from . import views
# from .feeds import UpdateFeed

DATE_PATTERN = '\d{4}-\d{2}-\d{2}'
MONTH_PATTERN = (
    'january|february|march|april|may|june|july|august|september|october|'
    'november|december'
)
YEAR_PATTERN = '\d{4}'


urlpatterns = [
    url(r'^$',
        views.SiteHome.as_view(),
        name='site_home'),

    url(r'^e(?P<pk>\d+)/$',
        views.RedirectToEvent.as_view(),
        name='events.event_redirect'),

    url(r'^(?P<slug>.+)/e(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='events.event_detail'),

    url(r'^about-thinking-liverpool/$',
        views.About.as_view(),
        name='events.about'),

    url(r'^whats-on-in-liverpool/$',
        views.EventList.as_view(),
        name='events.event_list'),

    url(r'^whats-on-in-liverpool/past-events/$',
        views.PastEventList.as_view(),
        name='events.past_events'),

    url(r'^whats-on-in-liverpool/(?P<month>' + MONTH_PATTERN
        + ')-(?P<year>' + YEAR_PATTERN + ')/$',
        views.MonthYearEventList.as_view(),
        name='events.month_year_event_list'),

    url(r'^whats-on-in-liverpool/(?P<slug>.+)/$',
        views.VenueEventList.as_view(),
        name='events.venue_event_list'),

    url(r'^u/(?P<date>' + DATE_PATTERN + ')/email-preview/$',
        views.UpdateEmailPreview.as_view(),
        name='events.update_email_preview'),

    # url(r'feed/rss/$', UpdateFeed()),
]
