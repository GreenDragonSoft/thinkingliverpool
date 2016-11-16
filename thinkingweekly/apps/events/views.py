import calendar
import datetime
import re

from icalendar import Calendar, Event as icalEvent

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.sites.models import Site

from .models import Event, Update, Venue, get_events_by_month


class SiteHome(TemplateView):
    template_name = 'events/site_home.html'

    def get_context_data(self):
        return {
            'next_event': self._get_next_event()
        }

    def _get_next_event(self):
        upcoming_events = Event.objects.filter(
            starts_at__gte=timezone.now(),
        ).order_by('starts_at')

        if upcoming_events.count():
            return upcoming_events[0]
        else:
            return None


class RedirectToEvent(View):
    model = Event

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['pk'])

        return redirect(event.get_absolute_url(), permanent=True)


class About(TemplateView):
    template_name = 'events/about.html'


class EventList(ListView):
    model = Event
    template_name = 'events/future_event_list.html'
    context_object_name = 'events'
    queryset = Event.objects.filter(
        starts_at__gte=timezone.now(),
    ).select_related('venue')


class EventDetail(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = "events/event_detail.html"


class PastEventList(TemplateView):
    template_name = 'events/past_event_list.html'

    def get_context_data(self):
        return {'months': get_events_by_month()}


class TEMPORARYMonthYearEventList(View):
    """
    TEMPORARY

    This view just exists to smooth the deletion of URLs like
    /whats-on-in-liverpool/december-2016/
    """

    def get(self, request, *args, **kwargs):
        month, year = self._get_month_year()

        if self.is_future():
            return redirect(
                reverse('events.event_list'),
                permanent=True,
            )
        else:
            month, year = self.kwargs['month'], self.kwargs['year']
            return redirect(
                reverse('events.past_events') + '#{}-{}'.format(month, year),
                permanent=True,
            )

    def is_future(self):
        month, year = self._get_month_year()
        last_day_of_month = datetime.date(
            year, month, calendar.monthrange(year, month)[1]
        )

        # return True until `now` is passed the end of the month
        return last_day_of_month > timezone.now().date()

    def _get_month_year(self):
        month = {
            'january': 1,
            'february': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6,
            'july': 7,
            'august': 8,
            'september': 9,
            'october': 10,
            'november': 11,
            'december': 12
        }[self.kwargs['month']]
        year = int(self.kwargs['year'])
        return month, year


class VenueEventList(DetailView):
    model = Venue
    context_object_name = 'venue'
    template_name = "events/venue_event_list.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(VenueEventList, self).get_context_data(
            *args, **kwargs)

        ctx['past_events'] = self.object.events.filter(
            starts_at__lte=timezone.now()
        ).order_by('-starts_at')

        ctx['future_events'] = self.object.events.filter(
            starts_at__gte=timezone.now()
        ).order_by('starts_at')
        return ctx


class UpdateEmailPreview(DetailView):
    model = Update
    context_object_name = 'update'
    template_name = "events/email/weekly_update.html"

    def get_object(self):
        return Update.objects.get(start_date=self.kwargs['date'])

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateEmailPreview, self).get_context_data(
            *args, **kwargs)
        ctx['events'] = self.object.events
        return ctx


class CalendarView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            self._make_ical(request),
            content_type='text/calendar'
        )
        response['Content-Disposition'] = (
            'attachment; filename="thinkingliverpool_{}.ics"'.format(
                timezone.now().date().isoformat()
            )
        )
        return response

    def _make_ical(self, request):
        one_month_ago = timezone.now() - datetime.timedelta(days=30)

        cal = Calendar()
        cal.add('prodid', '-//thinkingliverpool.com/calendar//EN')
        cal.add('version', '2.0')
        cal.add('X-WR-CALNAME', 'Thinking Liverpool')
        cal.add('X-WR-CALDESC', 'Events from www.thinkingliverpool.com')
        cal.add('X-WR-TIMEZONE', 'Europe/London')

        domain = re.sub('^www\.', '', Site.objects.get_current().domain)

        for event in Event.objects.filter(starts_at__gte=one_month_ago):
            event_url = request.build_absolute_uri(
                reverse('events.event_redirect', kwargs={'pk': event.id}))

            html_description = (
                '<a href="{url}">{shorter_url}</a>\n\n{desc}'.format(
                    url=event_url,
                    shorter_url=re.sub('^https?://www\.', '', event_url),
                    desc=event.description)
            )

            ical_event = icalEvent()
            ical_event.add('dtstamp', timezone.now())
            ical_event.add('created', event.created_at)
            ical_event.add('last-modified', event.updated_at)
            ical_event.add('uid', 'e{id}@{domain}'.format(
                id=event.id, domain=domain))
            ical_event.add('summary', event.title)
            ical_event.add('description', html_description)
            ical_event.add('X-ALT-DESC', html_description)
            ical_event.add('dtstart', event.starts_at)
            ical_event.add('location', event.venue.map_query)
            ical_event.add('url', event_url)
            cal.add_component(ical_event)
        return cal.to_ical()
