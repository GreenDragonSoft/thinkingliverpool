import datetime

from contextlib import contextmanager

import freezegun
import pytz

from django.test import TestCase

from nose.tools import assert_equal

from thinkingweekly.apps.events.models import (
    calculate_venue_sort_name, Venue, Event, Organiser
)


def test_calculate_venue_sort_name():
    assert_equal(
        'Florrie',
        calculate_venue_sort_name('The Florrie')
    )

    assert_equal(
        'Central Library',
        calculate_venue_sort_name('Liverpool Central Library')
    )

    assert_equal(
        'Foo The Bar',
        calculate_venue_sort_name('Foo The Bar')
    )


class TestEventTweet(TestCase):
    UK = pytz.timezone('Europe/London')

    MORNING = UK.localize(datetime.datetime(2016, 7, 29, 7, 30))
    EVENING = UK.localize(datetime.datetime(2016, 7, 29, 19, 30))

    WINTER_DATETIME = pytz.UTC.localize(
        datetime.datetime(2016, 1, 29, 16, 0))

    SUMMER_DATETIME = UK.localize(
        datetime.datetime(2016, 7, 28, 16, 0))

    @contextmanager
    def _make_event(self, starts_at, venue_twitter=None,
                    organiser=None, organiser_twitter=None, extra_twitter=None,
                    no_organiser=False, title='A talk'):

        venue = Venue.objects.create(
            name='Test Venue',
            address="123",
            twitter_handle=venue_twitter)

        if no_organiser:
            organiser = None
        else:
            organiser = Organiser.objects.create(
                name='Great people',
                twitter_handle=organiser_twitter)

        Event.objects.create(
            title=title,
            starts_at=starts_at,
            venue=venue,
            organiser=organiser,
            extra_twitter_handle=extra_twitter,
        )

        yield Event.objects.get()
        Event.objects.all().delete()
        Venue.objects.all().delete()
        Organiser.objects.all().delete()

    def test_morning_event(self):
        with self._make_event(starts_at=self.MORNING) as e:
            assert_equal(
                'A talk Fri 07:30 thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_evening_event(self):
        with self._make_event(starts_at=self.EVENING) as e:
            assert_equal(
                'A talk Fri 19:30 thinkingliverpool.com/e{}'.format(e.id),  # noqa',
                e.create_tweet()
            )  # noqa

    def test_venue_with_twitter_handle(self):
        with self._make_event(starts_at=self.EVENING,
                              venue_twitter='@venue') as e:
            assert_equal(
                'A talk Fri 19:30 @venue thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_with_no_organiser_set(self):
        with self._make_event(starts_at=self.EVENING, no_organiser=True) as e:
            assert_equal(
                'A talk Fri 19:30 thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_organiser_with_twitter_handle(self):
        with self._make_event(starts_at=self.EVENING,
                              organiser_twitter='@organiser') as e:
            assert_equal(
                'A talk Fri 19:30 @organiser thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_event_with_extra_twitter_handle(self):
        with self._make_event(starts_at=self.EVENING,
                              extra_twitter='@event') as e:
            assert_equal(
                'A talk Fri 19:30 @event thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_organiser_venue_and_event_with_twitter_handles(self):
        with self._make_event(starts_at=self.EVENING,
                              venue_twitter='@venue',
                              organiser_twitter='@organiser',
                              extra_twitter='@event') as e:

            assert_equal(
                'A talk Fri 19:30 @venue @organiser @event '
                'thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_duplicated_twitter_handles(self):
        with self._make_event(starts_at=self.EVENING,
                              venue_twitter='@dupe',
                              organiser_twitter='@dupe',
                              extra_twitter='@event') as e:

            assert_equal(
                'A talk Fri 19:30 @dupe @event thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_duplicated_twitter_handles_mixed_case(self):
        with self._make_event(starts_at=self.EVENING,
                              venue_twitter='@dupe',
                              organiser_twitter='@DUPE',
                              extra_twitter='@event') as e:

            assert_equal(
                'A talk Fri 19:30 @dupe @event thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_british_summer_time_event_queried_during_winter(self):
        with self._make_event(starts_at=self.SUMMER_DATETIME) as e, \
                freezegun.freeze_time('2016-01-01'):

            assert_equal(
                'A talk Thu 16:00 thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_british_summer_time_event_queried_during_summer(self):
        with self._make_event(starts_at=self.SUMMER_DATETIME) as e, \
                freezegun.freeze_time('2016-06-01'):
            assert_equal(
                'A talk Thu 16:00 thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_british_winter_time_event_queried_during_summer(self):
        with self._make_event(starts_at=self.WINTER_DATETIME) as e, \
                freezegun.freeze_time('2016-06-01'):
            assert_equal(
                'A talk Fri 16:00 thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_british_winter_time_event_queried_during_winter(self):
        with self._make_event(starts_at=self.WINTER_DATETIME) as e, \
                freezegun.freeze_time('2016-01-01'):
            assert_equal(
                'A talk Fri 16:00 thinkingliverpool.com/e{}'.format(e.id),  # noqa
                e.create_tweet()
            )

    def test_unicode(self):
        title = (
            'Test Γαζέες καὶ μυρτιὲς δὲν θὰ βρῶ πιὰ στὸ χρυσαφὶ ξέφωτο'
        )

        with self._make_event(starts_at=self.EVENING,
                              title=title) as e:
            assert_equal(
                'Test Γαζέες καὶ μυρτιὲς δὲν θὰ βρῶ πιὰ στὸ χρυσαφὶ ξέφωτο'
                ' Fri 19:30 thinkingliverpool.com/e{}'.format(e.id),  # noqa'
                e.create_tweet()
            )

    def test_too_long_truncates(self):
        title = (
            "this is a really long tweet that's going to go over the limit "
            "if we're not careful i'm not sure"
        )
        with self._make_event(starts_at=self.EVENING,
                              title=title,
                              venue_twitter='@venue',
                              organiser_twitter='@organiser',
                              extra_twitter='@event') as e:

            tweet = e.create_tweet()

            # supposedly the minimum number of characters twitter uses for a
            # URL is 23, so we can't ever be below that.

            assert_equal(140, len(tweet))
            assert_equal(
                "this is a really long tweet that's going to go over the "
                "limit if we're not car… Fri 19:30 @venue @organiser @event "
                "thinkingliverpool.com/e{}".format(e.id),  # noqa
                tweet
            )
