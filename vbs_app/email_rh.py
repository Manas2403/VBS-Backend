# vbs_app/views.py

from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_email_view(request,userEmail,message):
    username = "John"  # Example username
    context = {
               'message':message
               }
    email_html_message = render_to_string('booking_request.html', context)
    print(userEmail)
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        [userEmail],
        html_message=email_html_message,
    )
    print(email_html_message)
    # return render(request, 'vbs_app/booking_request.html', context)