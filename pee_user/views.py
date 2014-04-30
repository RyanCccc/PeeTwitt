from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from pee_user.models import PeeUser

# Create your views here.
def signup(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated() and user.is_active:
            return redirect('home')
        return render(request,'user/signup.html', {'error':''})
    elif request.method == 'POST':
        param = request.POST
        first_name = param.get('firstname')
        last_name = param.get('lastname')
        email = param.get('email')
        password = param.get('password')
        repassword = param.get('pwconfirm')
        if not first_name or not last_name:
            return render(request,'user/signup.html', {'error':'Please fill out all required fields'})
        if not email:
            return render(request,'user/signup.html', {'error':'Please fill out address'})
        if repassword != password:
            return render(request,'user/signup.html', {'error':'Password not same'})
        try:
            validate_email(email)
        except ValidationError:
            return render(request,'user/signup.html', {'error':'Please use correct email'})

        if User.objects.filter(email = email).exists():
            return render(request,'user/signup.html', {'error':'Email Exists'})
        else:
            my_user = PeeUser.objects.create_user(
                    email,
                    password,
                    first_name,
                    last_name,
            )
            request.POST = {'email':email}
            resend(request)
            return render(request,'user/signup.html', {'error':'', 'email':email})

@csrf_exempt
def resend(request):
    param = request.POST
    email = param.get('email')
    print email
    user = User.objects.get(email=email)
    my_user = user.peeuser
    verify_url = request.build_absolute_uri(reverse('pee_user_verify'))
    verify_url += '?' + 'key=' + my_user.active_key
    #import ipdb; ipdb.set_trace()
    print verify_url
    send_mail('Verification from PeeTwitt', 'Here is your verification url %s'%verify_url, 'purduetweet@gmail.com', [email,])
    result = json.dumps({'success':1})
    return HttpResponse(result, content_type="application/json")

def verify(request):
    param = request.GET
    key = param.get('key')
    if key:
        try:
            my_user = PeeUser.objects.get(active_key=key)
            user = my_user.user
            user.is_active = True
            user.save()
            return render(request,'index.html', {'error':'', 'success':True})
        except:
            return render(request,'index.html', {'error':'Activation key error', 'success':False})
    else:
        return render(request,'index.html', {'error':'No verification key', 'success':False})

def signin(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated() and user.is_active:
            return redirect('home')
        elif user.is_authenticated() and not user.is_active:
            context = {
                'next': request.GET.get('next'),
                'error':'',
                'email':user.peeuser.email,
            }
        else:
            context = {
                'next': request.GET.get('next'),
                'error':'',
            }
        return render(request,'index.html', context)
    elif request.method == 'POST':
        param = request.POST
        username = param.get('email')
        password = param.get('password')
        _next = param.get('next')
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return render(
                        request,'index.html',
                        {
                            'error':'Not verified yet!',
                            'email':user.email,
                        }
                    )
            login(request, user)
            if _next!='None' and _next:
                respond = redirect(_next)
            else:
                respond = redirect('home')
        else:
            return render(
                        request,'index.html',
                        {'error':'Incorrect login'}
                    )
        return respond

def signout(request):
    logout(request)
    return redirect('index')

# def upload_pic(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = PeeUser.objects.all()[0]
#             m.avatar = form.cleaned_data['image']
#             m.save()
#             html = '<html><head></head><body><img src="%s" alt="Smile"></body></html>'%m.avatar.url
#             return HttpResponse(html)
#     return HttpResponseForbidden('allowed only via POST')