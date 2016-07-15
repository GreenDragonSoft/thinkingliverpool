from django.views.generic.list import ListView
from django.utils import timezone

from .models import Event


class SiteHome(ListView):
    model = Event
    template_name = 'events/site_home.html'
    context_object_name = 'events'
    queryset = Event.objects.filter(
        starts_at__gte=timezone.now(),
    )
