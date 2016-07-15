from django.db import models
from autoslug import AutoSlugField


class Venue(models.Model):
    name = models.CharField(max_length=50)

    address = models.CharField(max_length=200)

    twitter_handle = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        help_text='With the leading @, eg @LEAFonBoldSt')

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
        max_length=15,
        help_text='With the leading @, eg @newsfromnowhere')

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

    organiser = models.ForeignKey(
        'Organiser',
        null=True,
        help_text=(
            'The group or organisations (if any) that organised this event. '
            'This may be the same as the venue, eg @LivUni and '
            '@newsfromnowhere or it may be separate, like how @Igniteliv '
            'is the organisation and they typically host in LEAF tea shop'
        )
    )
    venue = models.ForeignKey('Venue')

    extra_twitter_handle = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        default="",
    )

    description = models.TextField()

    def __str__(self):
        return self.title

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
