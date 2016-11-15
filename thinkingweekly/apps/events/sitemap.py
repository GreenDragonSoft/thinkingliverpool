import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Venue, Event


class ViewSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""

    def items(self):
        return [
            {
                'view': 'site_home',
                'changefreq': 'daily',
                'priority': 1.0,
            },
            {
                'view': 'events.event_list',
                'changefreq': 'daily',
                'priority': 1.0,
            },
            {

                'view': 'events.about',
                'changefreq': 'monthly',
            },
            {
                'view': 'events.past_events',
                'changefreq': 'monthly',
            }
        ]

    def location(self, item):
        return reverse(item['view'])

    def changefreq(self, item):
        return item['changefreq']

    def priority(self, item):
        return item.get('priority', 0.5)


class PastEventSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Event.objects.exclude(
            starts_at__date__gte=timezone.now().date()
        )

    def priority(self, event):
        if self._up_to_one_week_old(event):
            return 1.0
        else:
            return 0.5

    def changefreq(self, event):
        if self._up_to_one_week_old(event):
            return 'daily'

        elif self._one_week_to_one_month_old(event):
            return 'weekly'

        else:
            return 'monthly'

    @staticmethod
    def _up_to_one_week_old(event):
        return (
            PastEventSitemap._get_event_age(event) < datetime.timedelta(days=7)
        )

    @staticmethod
    def _one_week_to_one_month_old(event):
        age = PastEventSitemap._get_event_age(event)
        return datetime.timedelta(days=7) <= age < datetime.timedelta(days=30)

    @staticmethod
    def _get_event_age(event):
        return timezone.now() - event.starts_at


class VenueSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Venue.objects.exclude(slug__isnull=True).exclude(slug__exact='')
