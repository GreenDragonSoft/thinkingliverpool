from django.core.management.base import BaseCommand

from thinkingweekly.apps.events.schedule_helpers import create_updates


class Command(BaseCommand):
    help = ('Sends the most recent weekly update to Mailchimp')

    def handle(self, *args, **options):

        create_updates()
