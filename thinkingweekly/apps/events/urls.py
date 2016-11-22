from django.conf.urls import url
from django.views.generic import TemplateView
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

    url(r'^event/(?P<year>' + YEAR_PATTERN + ')/(?P<slug>.+)/e(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='events.event_detail'),

    url(r'^sign-up-thanks/$',
        TemplateView.as_view(template_name='events/sign_up_thanks.html'),
        name='events.sign_up_thanks'),

    url(r'^privacy/$',
        TemplateView.as_view(template_name='events/privacy.html'),
        name='events.privacy'),

    url(r'^about/$',
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
        views.TEMPORARYMonthYearEventList.as_view(),
        name='events.month_year_event_list'),

    url(r'^whats-on-in-liverpool/(?P<slug>.+)/$',
        views.VenueEventList.as_view(),
        name='events.venue_event_list'),

    url(r'^u/(?P<date>' + DATE_PATTERN + ')/email-preview/$',
        views.UpdateEmailPreview.as_view(),
        name='events.update_email_preview'),

    url(r'^update/(?P<date>' + DATE_PATTERN + ')/$',
        views.EmailUpdateArchive.as_view(),
        name='events.email_update_archive'),

    url(r'^calendar/$',
        views.CalendarView.as_view(),
        name='events.calendar'),

    # url(r'feed/rss/$', UpdateFeed()),
]
