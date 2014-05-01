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

from pee_user.models import PeeUser, ImageUploadForm
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


@login_required()
def following(request, pk):
    my_user = request.user.peeuser
    person = PeeUser.objects.get(pk=pk)
    pee_users = person.get_following()
    context = {
        'my_user':my_user,
        'person':person,
        'pee_users':pee_users,
        'title':'Following :',
    }
    return render(request, 'follow.html', context)

@login_required()
def followers(request, pk):
    my_user = request.user.peeuser
    person = PeeUser.objects.get(pk=pk)
    pee_users = person.get_followers()
    context = {
        'my_user':my_user,
        'person':person,
        'pee_users':pee_users,
        'title':'Followers :',
    }
    return render(request, 'follow.html', context)


def upload_avatar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = request.user.peeuser
            m.avatar = form.cleaned_data['image']
            next_url = form.cleaned_data['next_url']
            m.save()
            return redirect(next_url)
    return HttpResponseForbidden('allowed only via POST')