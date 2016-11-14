from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import Venue


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


class VenueSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Venue.objects.exclude(slug__isnull=True).exclude(slug__exact='')
