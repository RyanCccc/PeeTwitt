import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pee_user.models import PeeUser
from tweet.models import Tweet

def index(request):
    user = request.user
    if not user.is_anonymous():
        return redirect('home')
    return render(request,'index.html')

@login_required()
def home(request):
    user = request.user
    my_user = PeeUser.objects.get(user=user)
    followings = list(my_user.get_following())
    followings.append(my_user)
    tweets = Tweet.objects.filter(author__in=followings).order_by('-timestamp')
    context = {
        'my_user':my_user,
        'tweets': tweets,
        'title':'New Tweets :',
    }
    return render(request, 'home.html', context)