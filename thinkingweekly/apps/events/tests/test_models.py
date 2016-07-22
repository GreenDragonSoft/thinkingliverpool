from nose.tools import assert_equal
from thinkingweekly.apps.events.models import calculate_venue_sort_name


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
