from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone

from .models import Event, Update


class SiteHome(TemplateView):
    template_name = 'events/site_home.html'


class EventList(ListView):
    model = Event
    template_name = 'events/event_list.html'
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


class UpdateEmailPreview(DetailView):
    model = Update
    context_object_name = 'update'
    template_name = "events/email/weekly_update.html"

    def get_object(self):
        return Update.objects.get(start_date=self.kwargs['date'])

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateEmailPreview, self).get_context_data(*args, **kwargs)
        ctx['events'] = self.object.events
        return ctx
