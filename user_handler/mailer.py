from django.core.mail import send_mail
from django.conf import settings

def mail_it(data_json):
    send_mail(data_json['subject'], data_json['message'], settings.EMAIL_HOST_USER, data_json['to'])
    