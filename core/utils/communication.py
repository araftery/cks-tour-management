import textwrap

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from premailer import transform
from twilio.rest import TwilioRestClient

from core.utils.other import get_setting


def send_email(subject, to_emails, from_email, text_template, html_template, context, reply_to=None):
    plaintext = get_template(text_template)
    htmly = get_template(html_template)
    d = Context(context)

    if reply_to is None:
        reply_to = from_email

    text_content = plaintext.render(d)
    html_content = transform(htmly.render(d))
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails, headers={'Reply-To': reply_to})
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_text(to, template_name, context):
    account_sid = get_setting('Twilio Account SID')
    auth_token = get_setting('Twilio Auth Token')
    from_number = get_setting('Twilio Phone Number')

    client = TwilioRestClient(account_sid, auth_token)
    plaintext = get_template(template_name)
    d = Context(context)
    body = plaintext.render(d)
    bodies = textwrap.wrap(body, 160)
    for body in bodies:
        client.sms.messages.create(
            body=body,
            to=to,
            from_=from_number,
        )
