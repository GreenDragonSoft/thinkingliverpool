import datetime

from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.http import Http404

from .models import Event


class SiteHome(ListView):
    model = Event
    template_name = 'events/site_home.html'
    context_object_name = 'events'
    queryset = Event.objects.filter(
        starts_at__gte=timezone.now(),
    )


class CanonicalDetailViewMixin():
    def get(self, request, **kwargs):
        self.object = self.get_object()

        if self.request.path != self.object.get_absolute_url():
            return redirect(self.object)
        else:
            return super(CanonicalDetailViewMixin, self).get(request, **kwargs)


class EventDetail(CanonicalDetailViewMixin, DetailView):
    model = Event


def is_monday(dt):
    return dt.weekday() == 0


def is_future(date):
    return date > timezone.now().date()


class WeeklyUpdate(ListView):

    model = Event
    template_name = 'events/site_home.html'  # TODO
    context_object_name = 'events'

    def get(self, request, date):
        start_date = self.parse_date(date)
        if not is_monday(start_date) or is_future(start_date):
            raise Http404

        return super(WeeklyUpdate, self).get(request, date)

    def get_queryset(self):
        return Event.objects.filter(
            starts_at__gte=self.date_from(),
            starts_at__lt=self.date_to(),
        )

    def get_context_data(self):
        ctx = super(WeeklyUpdate, self).get_context_data()
        ctx['date_from'] = self.date_from()
        ctx['date_to'] = self.date_to()
        return ctx

    def date_from(self):
        return self.parse_date(self.kwargs['date'])

    def date_to(self):
        return self.date_from() + datetime.timedelta(days=14)

    @staticmethod
    def parse_date(date_string):
        return datetime.datetime.strptime(
           date_string, '%Y-%m-%d'
        ).date()


class WeeklyUpdateEmailPreview(WeeklyUpdate):
    template_name = "events/email/weekly_update.html"
