import datetime

from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Event


class WeeklyUpdateFeed(Feed):
    """
    Make an item for each event in the current update period (starting the
    most recent Monday, spanning 2 weeks)
    """

    def title(self):
        return "Talks and debates - Thinking Liverpool"

    def link(self):
        return ''

    def items(self):
        return Event.objects.filter(
            starts_at__gte=self._most_recent_monday(),
            starts_at__lt=self._most_recent_monday() + datetime.timedelta(days=14),
        )

    def item_description(self, item):
        return item.description

    def item_title(self, obj):
        return obj.title

    def _most_recent_monday(self):
        today = timezone.now().date()
        return today - datetime.timedelta(today.weekday())
