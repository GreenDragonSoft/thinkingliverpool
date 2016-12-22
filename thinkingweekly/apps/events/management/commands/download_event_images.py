from django.core.management.base import BaseCommand

from thinkingweekly.apps.events.helpers.download_images import (
    download_missing_images
)


class Command(BaseCommand):
    help = ('Attempts to download images from external_image_url fields')

    def handle(self, *args, **options):
        download_missing_images()
