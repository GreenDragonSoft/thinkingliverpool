import logging
import requests
import socket
import os

import backoff

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from thinkingweekly.apps.events.models import Event

LOG = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 10
USER_AGENT = 'thinkingliverpool.com/0.1 (bot@paulfurley.com)'

CONTENT_TYPES = {
    'image/jpeg': '.jpg',
}

REQUEST_EXCEPTIONS = (requests.exceptions.RequestException, socket.timeout)


class UnknownImageFileType(ValueError):
    pass


def download_missing_images():
    events_with_missing_images = Event.objects.filter(
        external_image_url__isnull=False,
        event_image=''
    )

    LOG.info("Getting images for {} events".format(
        events_with_missing_images.count()
    ))

    for event in events_with_missing_images.all():
        LOG.info("Getting image for {}".format(event))

        download_image_for_event(event)


def download_image_for_event(event):
    assert isinstance(event, Event), type(event)
    assert event.external_image_url is not None
    assert not bool(event.event_image)

    temp_file = download_image_as_temp_file(event.external_image_url)

    store_event_image(temp_file, event)


@backoff.on_exception(backoff.expo, REQUEST_EXCEPTIONS, max_tries=8)
def download_image_as_temp_file(url):
    LOG.info('Getting URL: {}'.format(url))
    response = requests.get(
        url,
        stream=True,  # makes response.content lazy
        timeout=DEFAULT_TIMEOUT,
        headers={'User-Agent': USER_AGENT},
    )

    response.raise_for_status()

    file_extension = derive_image_file_extension(response)

    if not file_extension:
        raise UnknownImageFileType(url)
    else:
        LOG.info("Using file extension: {}".format(file_extension))

    temp_file = NamedTemporaryFile(delete=True, suffix=file_extension)

    LOG.info('Writing response.content to {}'.format(temp_file.name))
    temp_file.write(response.content)
    temp_file.flush()
    return temp_file


def derive_image_file_extension(response):
    content_type_header = response.headers.get('content-type')
    LOG.info('Got content-type: {}'.format(content_type_header))

    return CONTENT_TYPES.get(
        content_type_header,
        os.path.splitext(response.request.url)[1]  # default to URL extension
    )


# @backoff.on_exception(backoff.expo,
#                       ??,  # Unclear which exceptions boto can raise
#                       max_tries=8)
def store_event_image(temp_file, event):

    base_filename = os.path.basename(temp_file.name)
    LOG.info("Uploading temporary file to storage: (base name {})".format(
        base_filename)
    )
    event.event_image.save(base_filename, File(temp_file))
