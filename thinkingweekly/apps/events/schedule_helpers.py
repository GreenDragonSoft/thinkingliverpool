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
from .email_helpers import send_update_by_email

LOG = logging.getLogger(__name__)


__all__ = [
    'create_updates',
    'post_events_twitter',
    'post_events_facebook',
    'post_update_email',
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


def post_update_email():
    if not _am_inside_update_post_time_window():
        LOG.info('Not inside event post time window')
        return

    update_to_post = _find_update_to_post_to_email()
    if update_to_post:
        _attempt_post_update_to_email_and_record(update_to_post)


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


def _attempt_post_update_to_email_and_record(update):
    LOG.info('Attempting to post update to email')
    try:
        with transaction.atomic():
            # record to database first; it can rollback
            _record_posted_update_to_email(update)
            _post_update_to_email(update)

    except Exception as e:
        LOG.exception(e)

        # TODO: don't mail admins from here, make an error logger which
        #       automatically emails them for this log level.
        mail_admins(
            'Failed to send email for {}'.format(update),
            repr(e),
            fail_silently=True)


def _post_update_to_email(update):
    LOG.info('Posting update to email: {}'.format(update))
    send_update_by_email(update)


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


def _am_inside_update_post_time_window():
    """
    We only attempt to post updates in the morning.
    """
    LOG.info("Time now: {}".format(timezone.now()))
    return 8 <= timezone.localtime(timezone.now()).hour <= 11


def _find_update_to_post_to_email():
    """
    Find updates which
    1. start from today or yesterday
    2. are marked as "ready"
    3. have not already been posted to email
    """

    now = timezone.now()
    today = timezone.localtime(now).date()
    yesterday = timezone.localtime(now - datetime.timedelta(days=1)).date()

    LOG.info('today: {} yesterday: {}'.format(today, yesterday))

    try:
        update = Update.objects.get(
            ready_to_post=True,
            have_posted_email=False,
            start_date__in=(today, yesterday),
        )
    except Update.DoesNotExist:
        LOG.info('No eligible Updates found.')
        return None

    if update.events.count() > 0:
        return update


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


def _record_posted_update_to_email(update):
    update.have_posted_email = True
    update.save()
