import collections
import logging

from django.template.defaulttags import register

LOG = logging.getLogger(__name__)


@register.filter(name='dict_get')
def dict_get(dictionary, key):
    if not isinstance(dictionary, collections.Mapping):
        LOG.warn('dict_get called with non-dictionary value `{}`'.format(
            dictionary))

        return None

    return dictionary.get(key)
