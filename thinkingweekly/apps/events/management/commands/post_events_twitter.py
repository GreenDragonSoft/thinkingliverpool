from django.core.management.base import BaseCommand

from thinkingweekly.apps.events.schedule_helpers import post_events_twitter


class Command(BaseCommand):
    help = ('Tweets out upcoming events and records them as posted.')

    def handle(self, *args, **options):

        post_events_twitter()
