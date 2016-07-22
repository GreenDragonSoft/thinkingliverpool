from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone

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
