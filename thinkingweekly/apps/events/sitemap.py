from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import Venue, get_events_by_month


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


class MonthYearSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            (x['name'], x['year'])
            for x in get_events_by_month()
        ]

    def location(self, month_year_tuple):
        month, year = month_year_tuple

        return reverse('events.month_year_event_list', kwargs={
            'month': month,
            'year': year,
        })


class VenueSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Venue.objects.exclude(slug__isnull=True).exclude(slug__exact='')
