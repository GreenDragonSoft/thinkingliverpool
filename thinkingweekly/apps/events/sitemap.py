from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Update, Venue, get_events_by_month


class UpdateSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Update.objects.filter(
            start_date__lte=timezone.now(),
            ready_to_post=True
        )

    # def lastmod(self, obj):
    #    return obj.updated_at=


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
