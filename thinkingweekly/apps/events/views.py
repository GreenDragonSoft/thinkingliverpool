import calendar
import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone

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


class MonthYearEventList(ListView):
    model = Event
    template_name = "events/month_year_event_list.html"
    context_object_name = 'events'

    def get_queryset(self, *args, **kwargs):
        month, year = self._get_month_year()

        return Event.objects.filter(
            starts_at__date__year=year,
            starts_at__date__month=month
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super(MonthYearEventList, self).get_context_data(
            *args, **kwargs)

        ctx['month'] = self.kwargs['month'].capitalize()
        ctx['year'] = int(self.kwargs['year'])

        ctx['is_future'] = self.is_future()
        return ctx

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
