from django.contrib import admin
from django.utils import timezone

from .models import Venue, Event, Organiser, Update


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'twitter_handle',
        'address',
        'website',
    )

    search_fields = (
        'name',
        'twitter_handle',
        'address',
        'website',
    )

    readonly_fields = (
        'sort_name',
    )

    ordering = ['sort_name']


@admin.register(Organiser)
class OrganiserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'twitter_handle',
        'website',
    )

    search_fields = (
        'name',
        'twitter_handle',
        'website',
    )

    ordering = ['name']


class PastEventsFilter(admin.SimpleListFilter):
    title = 'past events'

    parameter_name = 'starts_at'

    def lookups(self, request, model_admin):
        return (
            ('past events', 'past events'),
            ('future events', 'future events'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'past events':
            return queryset.filter(
                starts_at__lte=timezone.now()
            )

        elif self.value() == 'future events':
            return queryset.filter(
                starts_at__gte=timezone.now()
            )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'starts_at',
        'title',
        'description_brief',
        'venue',
        'event_image',
        'slug',
    )

    readonly_fields = [
        'slug',
    ]

    list_filter = [
        PastEventsFilter,
        ('venue', admin.RelatedOnlyFieldListFilter),
        ('organiser', admin.RelatedOnlyFieldListFilter),
    ]

    ordering = ('starts_at',)

    search_fields = (
        'title',
        'description',
    )


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'number_of_events',
        'ready_to_post',
        'have_posted_email',
    )

    readonly_fields = (
        'start_date',
        'end_date',
    )
