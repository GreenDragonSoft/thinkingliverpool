from django.core.mail import send_mail
from django.template import loader
from django.conf import settings


def send_update_by_email(update):
    assert update.events.count()

    subject_template = loader.get_template(
        'events/email/weekly_update_subject.txt'
    )

    body_template = loader.get_template(
        'events/email/weekly_update.html'
    )

    body = body_template.render({'update': update})
    subject = subject_template.render(
        {'date': update.start_date}
    ).strip('\r\n')

    # TODO
    from_address = 'Paul Furley <thinkingliverpool@paulfurley.com>'

    recipient_list = [
        settings.MAILCHIMP_EMAIL_BEAMER,
        'paul@paulfurley.com',  # TODO
    ]

    send_mail(
        subject,
        '<html email>',
        from_address,
        recipient_list,
        fail_silently=False,
        html_message=body,
    )
