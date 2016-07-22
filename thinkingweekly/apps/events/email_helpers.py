import datetime

from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from django.utils import timezone

from .models import Event


def send_weekly_update():

    subject_template = loader.get_template(
        'events/email/weekly_update_subject.txt'
    )

    body_template = loader.get_template(
        'events/email/weekly_update.html'
    )

    start_date = most_recent_monday()

    events = Event.objects.filter(
        starts_at__gte=start_date,
        starts_at__lt=start_date + datetime.timedelta(days=14),
    )

    body = body_template.render({'events': events})
    subject = subject_template.render({'date': start_date}).strip('\r\n')

    # TODO
    from_address = 'Paul Furley <thinkingliverpool@paulfurley.com>'

    recipient_list = [
        settings.MAILCHIMP_EMAIL_BEAMER
    ]

    send_mail(
        subject,
        '<html email>',
        from_address,
        recipient_list,
        fail_silently=False,
        html_message=body,
    )


def most_recent_monday():
    today = timezone.now().date()
    return today - datetime.timedelta(today.weekday())
