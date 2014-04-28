from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse

from pee_user.models import PeeUser

# Create your views here.
def signup(request):
    if request.method == 'GET':
        user = request.user
        if user.is_anonymous():
            return redirect('home')
        return render(request,'user/signup.html', {'error':'', 'succees':False})
    elif request.method == 'POST':
        param = request.POST
        first_name = param.get('first_name')
        last_name = param.get('last_name')
        email = param.get('email')
        password = param.get('password')
        repassword = param.get('repassword')
        if not email:
            return render(request,'user/signup.html', {'error':'Please fill out address', 'succees':False})
        if repassword != password:
            return render(request,'user/signup.html', {'error':'Password not same', 'succees':False})
        try:
            validate_email(email)
        except ValidationError:
            return render(request,'user/signup.html', {'error':'Please use correct email', 'succees':False})

        if User.objects.filter(username = username).exists():
            return render(request,'user/signup.html', {'error':'Username Exists', 'succees':False}
        else:
            my_user = PeeUser.objects.create_user(
                    email,
                    password,
                    first_name,
                    last_name,
            )
            return render(request,'user/signup.html', {'error':'', 'succees':True}