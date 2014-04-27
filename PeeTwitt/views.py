from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse

from pee_user.models import PeeUser

def index(request):
    user = request.user
    if not user.is_anonymous():
        return redirect('home')
    return render(request,'index.html')

@login_required()
def home(request):
    user = request.user
    if request.method == 'GET':
        my_user = PeeUser.objects.get(user=user)
        context = {
            'email' : user.email,
        }
        return render(request, 'home.html', context)