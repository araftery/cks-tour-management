from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from premailer import transform


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
