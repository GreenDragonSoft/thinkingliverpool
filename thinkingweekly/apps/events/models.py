import re

from django.db import models
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField


def calculate_venue_sort_name(venue_name):
    """
    Return venue name without certain leading words.
    We want eg "Liverpool Central Library" to sort next to "Central Library"
    """
    return re.sub(r'^((The|Liverpool)\s*)', '', venue_name)


class Venue(models.Model):
    name = models.CharField(max_length=50)

    sort_name = models.CharField(
        max_length=50,
        default='',
        editable=False,
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

    def save(self, *args, **kwargs):
        self.sort_name = self._calculate_sort_name()
        super(Venue, self).save(*args, **kwargs)

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
        ordering = ['-starts_at']

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

    venue = models.ForeignKey('Venue')

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'events.event_detail',
            kwargs={'pk': self.id, 'slug': self.slug}
        )

    def twitter_handles(self):
        handles = set([
            self.extra_twitter_handle,
            self.venue.twitter_handle,
        ])
        if self.organiser:
            handles.add(self.organiser.twitter_handle)

        return ' '.sort(handles)

    def description_brief(self):
        return self.description[0:50] + '…'
