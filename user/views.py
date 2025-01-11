from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse

from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required as lr

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from user.models import Profile

import string
import random

from datetime import datetime as dt
from datetime import timedelta 

import re

def log_in(request):

    c = {}

    c['u'] = request.user

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        c['m'] = True
    else:
        c['m'] = False

    if request.method == 'POST':

        u = authenticate(

            username = request.POST.get('u').lower(),
            password = request.POST.get('p'),

        )

        if u:

            login(request, u)
            return redirect('/home')

        else: 

            return render(request, 'auth/login.html', {'e': True})
    
    return render(request, 'auth/login.html', c)

def register(request):

    c = {}

    c['u'] = request.user

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        c['m'] = True
    else:
        c['m'] = False

    if request.method == 'POST':

        name = request.POST.get('n')

        username = request.POST.get('u').lower()
        password = request.POST.get('p')

        user = User(username = username)
        user.set_password(password)
        user.save()

        user.profile.name = name
        user.profile.initials = ''.join(letter[0].upper() for letter in name.split(' '))[0:3]

        uid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))

        while True:
            if Profile.objects.filter(premium_invite_uid = uid).exists():
                uid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
            else:
                break

        user.profile.premium_invite_uid = uid
        user.profile.save()

        user = authenticate(username = username, password = password)
        login(request, user)
        

        return redirect('/')

    return render(request, 'auth/register.html', c)

def log_out(request):

    logout(request)

    return redirect('/')