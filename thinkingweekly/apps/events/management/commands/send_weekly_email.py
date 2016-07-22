from django.core.management.base import BaseCommand

from thinkingweekly.apps.events.email_helpers import send_weekly_update


class Command(BaseCommand):
    help = ('Sends the most recent weekly update to Mailchimp')

    def handle(self, *args, **options):

        send_weekly_update()
