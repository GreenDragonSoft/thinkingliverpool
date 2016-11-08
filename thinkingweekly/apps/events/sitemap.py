from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import Venue, get_events_by_month


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
    priority = 0.7

    def items(self):
        return Venue.objects.exclude(slug__isnull=True).exclude(slug__exact='')
