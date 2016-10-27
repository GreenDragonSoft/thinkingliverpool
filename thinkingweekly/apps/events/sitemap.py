from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import Update


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