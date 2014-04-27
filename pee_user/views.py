from django.shortcuts import render, redirect
from decorators import guest_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse

from pee_user.models import PeeUser

# Create your views here.
@guest_required
def signup(request):
    if request.method == 'GET':
        return render(request,'user/signup.html', {'error':''})
    elif request.method == 'POST':
        param = request.POST
        email = param.get('email')
        password = param.get('password')
        repassword = param.get('repassword')
        if not email:
            return render(request,'user/signup.html', {'error':'Please fill out address'})
        if repassword != password:
            return render(request,'user/signup.html', {'error':'Password not same'})
        try:
            validate_email(email)
        except ValidationError:
            return render(request,'user/signup.html', {'error':'Please use correct email'})

        if User.objects.filter(username = username).exists():
            user = User.objects.get(username = username)
            if user.is_active:
                return render(request,'user/signup.html', {'error':'Username Exists'})
            else:
                ## TODO
                #return render(request,'user/signup.html', {'error':'Username Exists'})
                pass
        else:
            my_user = PeeUser.objects.create_user(
                    email,
                    password,
            )
            user = my_user.user
            user = authenticate(username=username, password=password)
            login(request, user)
            respond = redirect('home')
            return respond


            