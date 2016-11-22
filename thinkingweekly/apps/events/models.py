import datetime
import re

from urllib.parse import urlparse

from django.db import models
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils import formats, timezone
from django.utils.http import urlquote_plus

from autoslug import AutoSlugField


def calculate_venue_sort_name(venue_name):
    """
    Return venue name without certain leading words.
    We want eg "Liverpool Central Library" to sort next to "Central Library"
    """
    return re.sub(r'^((The|Liverpool)\s*)', '', venue_name)


def get_events_by_month():
    def get_events_for(month, year):
        return Event.objects.filter(
            starts_at__date__year=year,
            starts_at__date__month=month,
        )

    try:
        earliest_event = Event.objects.all().order_by('starts_at')[0]
        earliest_date = earliest_event.starts_at.date()
    except KeyError:
        return

    this_month_mid = (
        timezone.now().date().replace(day=14)
    )

    for i in range(0, 20 * 12):  # just-in-case limit to 20 years
        day = (
            this_month_mid - (i * datetime.timedelta(days=30.5))
        ).replace(day=14)

        if day < earliest_date:
            break  # finished!

        yield {
            'name': day.strftime('%B').lower(),   # 'november'
            'month': day.month,                   # 11
            'year': day.year,                     # 2016
            'events': get_events_for(day.month, day.year)
        }
    else:
        raise RuntimeError("This shouldn't happen: we ierated past earliest "
                           "date ({}).".format(earliest_date))
        pass


class Venue(models.Model):
    name = models.CharField(max_length=50)

    sort_name = models.CharField(
        max_length=50,
        default='',
        editable=False,
    )

    slug = models.SlugField(
        default=None,
        null=True,
        blank=True,
        help_text=(
            "Add this to give the venue its own web page. Add with care, "
            "since it shouldn't be changed after it's set."
        )
    )

    address = models.CharField(max_length=200)

    twitter_handle = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        help_text='With the leading @, eg @LEAFonBoldSt')

    website = models.URLField(
        null=True,
        blank=True,
    )

    @property
    def twitter_url(self):
        if self.twitter_handle:
            return 'https://twitter.com/{}'.format(
                self.twitter_handle.lstrip('@')
            )

    @property
    def map_url(self):
        return 'http://maps.google.co.uk/maps?q={}'.format(
            urlquote_plus(self.map_query)
        )

    @property
    def map_query(self):
        return self.name + ', ' + self.address

    def save(self, *args, **kwargs):
        self.sort_name = self._calculate_sort_name()
        super(Venue, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'events.venue_event_list',
            kwargs={'slug': self.slug}
        )

    def _calculate_sort_name(self):
        return calculate_venue_sort_name(self.name)

    def __str__(self):
        if self.twitter_handle:
            return '{} ({})'.format(self.name, self.twitter_handle)
        else:
            return '{}'.format(self.name)


class Organiser(models.Model):
    name = models.CharField(max_length=50)
    twitter_handle = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        help_text='With the leading @, eg @newsfromnowhere')

    website = models.URLField(
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.twitter_handle:
            return '{} ({})'.format(self.name, self.twitter_handle)
        else:
            return '{}'.format(self.name)


class Event(models.Model):
    class Meta:
        ordering = ['starts_at']

    title = models.CharField(max_length=100)

    id = models.AutoField(primary_key=True)
    slug = AutoSlugField(populate_from='title')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_url = models.URLField(
        help_text=(
            'Ideally this should be a URL for the event itself (not the '
            'general website of the organiser) and it should be the '
            'authoritative source of the event, '
            'not some other site that links to it. '
            'If there is no single URL then a more general URL can be used, '
            'like the website of the organisation.'
        ),
    )

    starts_at = models.DateTimeField(
        help_text=(
            'The time the event starts, or if it says to arrive early, then '
            'the arrival time'
        )
    )

    venue = models.ForeignKey('Venue', related_name='events')

    organiser = models.ForeignKey(
        'Organiser',
        null=True,
        blank=True,
        help_text=(
            '*IF different from the Venue, the group or organisations (if '
            'any) that organised this event, for example @Igniteliv '
            'is the organisation beind Ignite, which is usually hosted in '
            'LEAF tea shop'
        )
    )

    extra_twitter_handle = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        default=None,
    )

    description = models.TextField()

    have_posted_facebook = models.BooleanField(default=False)

    have_posted_twitter = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_future_url(self):
        return reverse('events.event_list') + '#{}'.format(self.slug)

    def get_absolute_url(self):
        return reverse(
            'events.event_detail',
            kwargs={
                'pk': self.id,
                'slug': self.slug,
                'year': self.starts_at.date().year,
            }
        )

    def is_future(self):
        return self.starts_at.date() > timezone.today()

    def twitter_handles(self):
        handles = filter(None, [
            self.venue.twitter_handle,
            self.organiser.twitter_handle if self.organiser else None,
            self.extra_twitter_handle,
        ])

        def f7(seq):
            seen = set()
            return [x for x in seq
                    if not (x.lower() in seen or seen.add(x.lower()))]

        return ' '.join(f7(handles))

    def external_domain(self):
        parsed_uri = urlparse(self.external_url)
        return re.sub(r'^www\.', '', parsed_uri.netloc)

    def description_brief(self):
        return self.description[0:50] + '…'

    def create_tweet(self):
        when = timezone.localtime(self.starts_at).strftime('%a %H:%M')
        twitters = self.twitter_handles()

        TWEET_LENGTH = 140
        URL_LENGTH = len('thinkingliverpool.com/e') + len(str(self.id))

        available_characters = TWEET_LENGTH - (
            URL_LENGTH + len(twitters) + len(when) + 3)

        def truncate(string, length):
            if len(string) > length:
                return string[0:length-1] + '…'
            else:
                return string

        title = truncate(self.title, available_characters)

        return ' '.join(filter(None, [
            title,
            when,
            twitters,
            'thinkingliverpool.com/e{}'.format(self.id),
        ]))


class Update(models.Model):
    class Meta:
        unique_together = ('start_date', 'end_date')
        ordering = ('start_date',)

    start_date = models.DateField(
        primary_key=True
    )

    end_date = models.DateField()

    ready_to_post = models.BooleanField(
        help_text=(
            'Enable this to schedule the update to be posted '
            'automatically (betweem 9am-11am on Monday).'
        ),
        default=False,
    )

    have_posted_email = models.BooleanField(
        # Once we're using the Mailchimp API, this could turn into a
        # MailchimpCampaign model to record the details, then later track
        # analytics.
        default=False
    )

    have_posted_facebook = models.BooleanField(default=False)

    have_posted_twitter = models.BooleanField(default=False)

    def __str__(self):
        return 'Update({} to {})'.format(
            formats.date_format(self.start_date),
            formats.date_format(self.end_date),
        )

    @property
    def events(self):
        # For now I think it's safe to dynamically generate the list of events
        # rather than storing them separately against an update.

        return Event.objects.filter(
            starts_at__gte=self.start_date,
            starts_at__lt=self.end_date,
        )

    @property
    def number_of_events(self):
        return self.events.count()

    def get_url(self):
        """
        Return the (actual) absolute URL, with protocol & domain.
        https://code.djangoproject.com/wiki/ReplacingGetAbsoluteUrl
        """
        domain = Site.objects.get_current().domain

        return 'https://{}{}'.format(domain, self.get_url_path())

    def get_url_path(self):
        return reverse(
            'events.email_update_archive',
            kwargs={'date': self.start_date}
        )

    def get_absolute_url(self):
        """
        Bad name (https://code.djangoproject.com/wiki/ReplacingGetAbsoluteUrl)
        Return the url path.
        """
        return self.get_url_path()
