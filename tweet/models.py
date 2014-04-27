from django.db import models
from pee_user.models import PeeUser

# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(PeeUser)
    content = models.CharField(max_length=140)
    timestamp = models.DateField(auto_now_add=True)


class Reply(models.Model):
    author = models.ForeignKey(PeeUser)
    tweet = models.ForeignKey(Tweet)
    content = models.CharField(max_length=140)
    timestamp = models.DateField(auto_now_add=True)
