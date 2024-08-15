from threading import Thread

from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token
from superlists.settings import EMAIL_HOST_USER


def send_async_login_email(subject, message, from_email, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[email],
    )


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid),
    )
    message_body = f"Use this link to log in:\n\n{url}"
    
    thr = Thread(target=send_async_login_email,
                 args=[
                     'Your login link for Superlists',
                     message_body,
                     EMAIL_HOST_USER,
                     email
                 ]
                 )
    thr.start()
    
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    
    return redirect("/")


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
