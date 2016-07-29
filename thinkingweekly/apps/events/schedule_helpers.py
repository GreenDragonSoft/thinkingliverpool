"""
Currently, we have an "Update" which starts each Monday and covers the next
two week period. (start_date, end_date)

We post Updates by email & social media at 9am on the start date.
"""

import datetime
import logging

from django.utils import timezone

from thinkingweekly.apps.events.models import Update

LOG = logging.getLogger(__name__)


__all__ = [
    'create_updates',
    'post_events_twitter',
    'post_events_facebook',
    'post_update_twitter',
    'post_update_facebook',
]


def create_updates():
    """
    Create (if required) an Update object for the previous Monday and the
    upcoming Monday. That ensures we have next week's update ready to
    tinker with (adding custom text, for example) for a whole week before it
    goes out.
    """
    today = timezone.now().date()
    current_monday = today - datetime.timedelta(days=today.weekday())
    next_monday = current_monday + datetime.timedelta(days=7)

    _ensure_update_exists(current_monday)
    _ensure_update_exists(next_monday)


def _ensure_update_exists(start_monday):
    (update, created) = Update.objects.get_or_create(
        start_date=start_monday,
        defaults={
            'end_date': start_monday + datetime.timedelta(days=14)
        }
    )

    if created:
        LOG.info("Created {}".format(update))


def post_events_twitter():
    pass


def post_events_facebook():
    pass


def post_update_twitter():
    pass


def post_update_facebook():
    pass
