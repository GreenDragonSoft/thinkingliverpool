"""
Currently, we have an "Update" which starts each Monday and covers the next
two week period. (start_date, end_date)

We post Updates by email & social media at 9am on the start date.
"""

import datetime
import logging

from django.utils import timezone
from django.db import transaction
from django.conf import settings

from django.core.mail import mail_admins

import tweepy

from thinkingweekly.apps.events.models import Event, Update

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
    if not _am_inside_event_post_time_window():
        return

    for event in _find_events_to_post_to_twitter():
        _attempt_post_and_record_to_twitter(event)


def _attempt_post_and_record_to_twitter(event):
    try:
        with transaction.atomic():
            _post_event_to_twitter(event)
            _record_posted_event_to_twitter(event)

    except Exception as e:
        LOG.exception(e)

        # TODO: don't mail admins from here, make an error logger which
        #       automatically emails them for this log level.
        mail_admins(
            'Failed to send tweet for {}'.format(event),
            repr(e),
            fail_silently=True)


def post_events_facebook():
    pass


def post_update_twitter():
    pass


def post_update_facebook():
    pass


def _am_inside_event_post_time_window():
    """
    We only attempt to tweet out events between 1pm and 5pm.
    """
    LOG.info("Time: {}".format(timezone.now()))
    return 13 <= timezone.now().hour <= 18


def _find_events_to_post_to_twitter():
    """
    Return events which
    1. havent been posted
    2. start tomorrow
    """
    LOG.info("Looking for events")
    tomorrow = timezone.now().date() + datetime.timedelta(days=1)

    return Event.objects.filter(
        have_posted_twitter=False,
        starts_at__date=tomorrow,
    )


def _post_event_to_twitter(event):
    status = event.create_tweet()

    LOG.info("Posting to Twitter: {}: '{}'".format(event, status))

    api = get_authenticated_twitter_api()
    api.update_status(status=status)


def get_authenticated_twitter_api():
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def _record_posted_event_to_twitter(event):
    event.have_posted_twitter = True
    event.save()
